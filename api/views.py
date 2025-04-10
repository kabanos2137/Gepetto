import os

from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from dotenv import load_dotenv
from Crypto import Random

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import base64
import uuid

from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED, \
    HTTP_405_METHOD_NOT_ALLOWED, HTTP_401_UNAUTHORIZED

from api.decorators import require_auth
from api.models import UserCredentials, Assistant, AssistantPermissions, Conversation, ConversationPermissions, \
    ConversationMessage, UserTokens
from openai import AzureOpenAI

load_dotenv("./.confidential.env")

client = AzureOpenAI(
    azure_endpoint=os.getenv('OPENAI_API_BASE'),
    api_key=os.getenv('OPENAI_API_KEY'),
    api_version="2024-05-01-preview",
)

def build_system_prompt(description: str, response_style: str, tone: str) -> str:
    return (
        f"You are an assistant with the following role: {description}.\n"
        f"Respond in a {response_style} style and keep your tone {tone}.\n"
        f"Adapt your language and structure accordingly."
    )

@api_view(['GET', 'POST'])
def user(_request):
    if _request.method == "GET":
        if "username" in _request.GET:
            if "email" in _request.GET:
                try:
                    _user = UserCredentials.objects.filter(name=_request.GET["username"], email=_request.GET["email"]).get()
                except UserCredentials.DoesNotExist:
                    return Response(
                        {
                            "found": False,
                            "message": "No user with given username and email was found"
                        },
                        status=HTTP_404_NOT_FOUND
                    )

                return Response(
                    {
                        "found": True
                    },
                    status=HTTP_200_OK
                )
            else:
                try:
                    _user = UserCredentials.objects.filter(name=_request.GET["username"]).get()
                except UserCredentials.DoesNotExist:
                    return Response(
                        {
                            "found": False,
                            "message": "No user with given username was found"
                        },
                        status=HTTP_404_NOT_FOUND
                    )

                return Response(
                    {
                        "found": True
                    },
                    status=HTTP_200_OK
                )
        else:
            if "email" in _request.GET:
                try:
                    _user = UserCredentials.objects.filter(email=_request.GET["email"]).get()
                except UserCredentials.DoesNotExist:
                    return Response(
                        {
                            "found": False,
                            "message": "No user with given email was found"
                        },
                        status=HTTP_404_NOT_FOUND
                    )

                return Response(
                    {
                        "found": True
                    },
                    status=HTTP_200_OK
                )
            else:
                return Response(
                    {
                        "found": False,
                        "message": "No username or email was provided"
                    },
                    status=HTTP_400_BAD_REQUEST
                )
    elif _request.method == "POST":
        try:
            _user = UserCredentials.objects.filter(Q(name=_request.data["username"]) | Q(email=_request.data["email"])).get()
        except UserCredentials.DoesNotExist:
            _encrypted_password = _request.data['password']
            _encrypted_bytes = base64.b64decode(_encrypted_password)

            with open("private.pem", "r") as _f:
                _private_key = RSA.import_key(_f.read())
            _cipher = PKCS1_v1_5.new(_private_key)
            _sentinel = Random.get_random_bytes(32)
            _decrypted_password = _cipher.decrypt(_encrypted_bytes, _sentinel).decode("utf-8")

            UserCredentials.objects.create(
                name=_request.data["username"],
                password=make_password(_decrypted_password),
                email=_request.data["email"]
            )

            return Response(
                {
                    'created': True
                },
                status=HTTP_201_CREATED
            )

        return Response(
            {
                "created": False,
                "message": "Either username or email is already used"
            },
            status=HTTP_400_BAD_REQUEST
        )
    else:
        return Response(
            {
                "message": "Method not allowed"
            },
            status=HTTP_405_METHOD_NOT_ALLOWED
        )

@api_view(['POST'])
def login(_request):
    if _request.method == "POST":
        _username = _request.data['username']
        _encrypted_password = _request.data['password']

        _encrypted_bytes = base64.b64decode(_encrypted_password)

        with open("private.pem", "r") as _f:
            _private_key = RSA.import_key(_f.read())
        _cipher = PKCS1_v1_5.new(_private_key)
        _sentinel = Random.get_random_bytes(32)
        _decrypted_password = _cipher.decrypt(_encrypted_bytes, _sentinel).decode("utf-8")

        _user = UserCredentials.objects.filter(name=_username)
        if _user.exists() and _username != "assistant" and check_password(_decrypted_password, _user.get().password):
            token = str(uuid.uuid4())

            UserTokens.objects.create(
                user = _user.get(),
                token = token
            )

            return Response({
                "found": True,
                "token": token
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "found": False
            }, status=status.HTTP_200_OK)
    else:
        return Response(
            {
                "message": "Method not allowed"
            },
            status=HTTP_405_METHOD_NOT_ALLOWED
        )

@api_view(['POST', 'GET'])
@require_auth
def assistant(_request):
    if _request.method == "POST":
        _name = _request.data['assistant_name']
        _description = _request.data['description']
        _response_style = _request.data['response_style']
        _tone = _request.data['tone']
        _profile_picture = _request.data['profile_picture']

        _assistant = Assistant.objects.create(
            name = _name,
            description = _description,
            response_style = _response_style,
            tone = _tone,
            profile_picture = _profile_picture
        )

        AssistantPermissions.objects.create(
            user = _request.user,
            assistant = _assistant,
            can_edit = True,
            can_delete = True,
            can_view = True,
        )

        return Response(
            {
                "assistant_id": _assistant.id
            },
            status=HTTP_201_CREATED
        )
    elif _request.method == "GET":
        if "assistant_id" in _request.GET:
            try:
                _assistant = Assistant.objects.filter(id = _request.GET["assistant_id"]).get()
            except Assistant.DoesNotExist:
                return Response(
                    {
                        "message": "Assistant not found",
                        "action": "REDIR_TO_APP"
                    },
                    status=HTTP_404_NOT_FOUND
                )

            try:
                _assistant_permission = AssistantPermissions.objects.filter(
                    user = _request.user,
                    assistant = _assistant,
                    can_view = True,
                )
            except AssistantPermissions.DoesNotExist:
                return Response(
                    {
                        "message": "You do not have permissions to this assistant",
                        "action": "REDIR_TO_APP"
                    },
                    status=HTTP_401_UNAUTHORIZED
                )

            return Response(
                {
                    "assistant_id": _assistant.id,
                    "assistant_name": _assistant.name,
                    "description": _assistant.description,
                    "response_style": _assistant.response_style,
                    "tone": _assistant.tone,
                    "profile_picture": _assistant.profile_picture,
                },
                status=HTTP_200_OK
            )
        else:
            _permissions = AssistantPermissions.objects.filter(user=_request.user, can_view=True)

            _assistants = []

            for _permission in _permissions:
                _assistants.append({
                    "id": _permission.assistant.id,
                    "name": _permission.assistant.name,
                    "description": _permission.assistant.description,
                    "response_style": _permission.assistant.response_style,
                    "tone": _permission.assistant.tone,
                    "profile_picture": _permission.assistant.profile_picture,
                })

            return Response(
                {
                    "assistants": _assistants
                },
                status = status.HTTP_200_OK
            )
    else:
        return Response(
            {
                "message": "Method not allowed",
                "action": "REDIR_TO_APP"
            },
            status=HTTP_405_METHOD_NOT_ALLOWED
        )

@api_view(['POST', 'GET'])
@require_auth
def conversation(_request):
    if _request.method == "POST":
        try:
            _assistant = Assistant.objects.filter(id = _request.data["assistant_id"]).get()
        except Assistant.DoesNotExist:
            return Response(
                {
                    "message": "Assistant not found",
                    "action": "REDIR_TO_APP"
                },
                status=HTTP_404_NOT_FOUND
            )

        try:
            _assistant_permissions = AssistantPermissions.objects.filter(user = _request.user, assistant = _assistant, can_edit = True).get()
        except AssistantPermissions.DoesNotExist:
            return Response(
                {
                    "message": "You do not have permissions to this assistant",
                    "action": "REDIR_TO_APP"
                },
                status=HTTP_401_UNAUTHORIZED
            )

        _conversation = Conversation.objects.create(
            name = _request.data["conversation_name"],
            assistant = _assistant,
        )

        ConversationPermissions.objects.create(
            user = _request.user,
            conversation = _conversation,
            can_edit = True,
            can_delete = True,
            can_view = True
        )

        return Response(
            {
                "conversation_id": _conversation.id
            },
            status=HTTP_201_CREATED
        )
    elif _request.method == "GET":
        if "conversation_id" in _request.GET:
            try:
                _conversation = Conversation.objects.filter(id = _request.GET["conversation_id"]).get()
            except Conversation.DoesNotExist:
                return Response(
                    {
                        "message": "Conversation not found",
                        "action": "REDIR_TO_APP"
                    },
                    status=HTTP_404_NOT_FOUND
                )

            try:
                _conversation_permissions = ConversationPermissions.objects.filter(user = _request.user, conversation = _conversation, can_view = True).get()
            except ConversationPermissions.DoesNotExist:
                return Response(
                    {
                        "message": "You do not have permissions to this conversation",
                        "action": "REDIR_TO_APP"
                    },
                    status=HTTP_401_UNAUTHORIZED
                )

            _messages = ConversationMessage.objects.filter(conversation = _conversation)

            return Response(
                {
                    "conversation_id": _conversation.id,
                    "conversation_name": _conversation.name,
                    "date_of_creation": _conversation.date_of_creation,
                    "assistant_id": _conversation.assistant.id,
                    "assistant_name": _conversation.assistant.name,
                    "messages": [
                        {
                            "message_id": _message.id,
                            "message": _message.message,
                            "date_of_creation": _message.date_of_creation,
                            "sent_by": _message.sent_by.id,
                            "sent_by_name": _message.sent_by.name
                        } for _message in _messages
                    ]
                },
                status=HTTP_200_OK
            )
        else:
            try:
                _assistant = Assistant.objects.filter(id = _request.GET["assistant_id"]).get()
            except Assistant.DoesNotExist:
                return Response(
                    {
                        "message": "Assistant not found",
                        "action": "REDIR_TO_APP"
                    },
                    status=HTTP_404_NOT_FOUND
                )

            try:
                _asssistant_permissions = AssistantPermissions.objects.filter(user = _request.user, assistant = _assistant, can_view = True).get()
            except AssistantPermissions.DoesNotExist:
                return Response(
                    {
                        "message": "You do not have permission to this assistant",
                        "action": "REDIR_TO_APP"
                    }
                )

            _conversation_permissions = ConversationPermissions.objects.filter(user = _request.user, can_view = True)

            _conversations = []

            for _conversation_permission in _conversation_permissions:
                _conversation = _conversation_permission.conversation
                if _conversation.assistant.id == _assistant.id:
                    _conversations.append({
                        "id": _conversation.id,
                        "name": _conversation.name,
                        "date_of_creation": _conversation.date_of_creation,
                    })

            return Response(
                {
                    "conversations": _conversations,
                },
                status=HTTP_200_OK
            )
    else:
        return Response(
            {
                "message": "Method not allowed",
                "action": "REDIR_TO_APP"
            },
            status=HTTP_405_METHOD_NOT_ALLOWED
        )

@api_view(['POST'])
@require_auth
def message(_request):
    if _request.method == "POST":
        try:
            _conversation = Conversation.objects.filter(id = _request.data["conversation_id"]).get()
        except Conversation.DoesNotExist:
            return Response(
                {
                    "message": "Conversation not found",
                    "action": "REDIR_TO_APP"
                },
                status=HTTP_404_NOT_FOUND
            )

        try:
            _conversation_permission = ConversationPermissions.objects.filter(user = _request.user, conversation = _conversation, can_edit = True).get()
        except ConversationPermissions.DoesNotExist:
            return Response(
                {
                    "message": "You do not have permissions to this conversation",
                    "action": "REDIR_TO_APP"
                },
                status=HTTP_401_UNAUTHORIZED
            )

        ConversationMessage.objects.create(
            conversation = _conversation,
            message = _request.data["message"],
            sent_by = _request.user,
        )

        _raw_messages = ConversationMessage.objects.filter(conversation = _conversation)

        _messages = [{
            "role": "system",
            "content": build_system_prompt(_conversation.assistant.description, _conversation.assistant.response_style, _conversation.assistant.tone),
        }]

        for _message in _raw_messages:
            _messages.append({
                "role": "assistant" if _message.sent_by.id == 0 else "user",
                "content": _message.message,
            })

        _response = client.chat.completions.create(
            model = "gpt-4-ai-model",
            messages = _messages,
            max_tokens = 1500
        )

        ConversationMessage.objects.create(
            conversation = _conversation,
            message = _response.choices[0].message.content,
            sent_by = UserCredentials.objects.filter(id = 0).get()
        )

        return Response(
            {
                "message": _response.choices[0].message.content,
            },
            status=HTTP_200_OK
        )
    else:
        return Response(
            {
                "message": "Method not allowed",
                "action": "REDIR_TO_APP"
            },
            status=HTTP_405_METHOD_NOT_ALLOWED
        )

@api_view(["GET"])
def public_key(_request):
    with open("public.pem", "r") as f:
        public_key = f.read()
    return Response(
        {
            "public_key": public_key
        },
        status=status.HTTP_200_OK
    )