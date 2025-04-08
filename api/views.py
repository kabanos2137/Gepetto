import os

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from dotenv import load_dotenv
from Crypto import Random

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import base64

from api.models import UserCredentials, Assistant, AssistantPermissions, Conversation, ConversationPermissions, \
    ConversationMessage
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
    if _request.method == 'GET':
        if "username" in _request.GET and "email" in _request.GET:
            _username = _request.GET["username"]
            _email = _request.GET["email"]

            _user = UserCredentials.objects.filter(name=_username, email=_email)
            if _user.exists():
                return Response({
                    "found": True
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "found": False
                }, status=status.HTTP_200_OK)
        elif "username" in _request.GET:
            _username = _request.GET["username"]

            _user = UserCredentials.objects.filter(name=_username)
            if _user.exists():
                return Response({
                    "found": True
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "found": False
                }, status=status.HTTP_200_OK)
        elif "email" in _request.GET:
            _email = _request.GET["email"]

            _user = UserCredentials.objects.filter(email=_email)
            if _user.exists():
                return Response({
                    "found": True
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "found": False
                }, status=status.HTTP_200_OK)
        else:
            return Response({
                "found": False
            }, status=status.HTTP_400_BAD_REQUEST)
    elif _request.method == 'POST': # check if request method is POST
        _username = _request.data['username'] # get username from request
        _password = _request.data['password'] # get password from request
        _email = _request.data['email'] # get email from request

        _user_exists = UserCredentials.objects.filter(name=_username).exists() or UserCredentials.objects.filter(email=_email).exists() # check if user already exists

        if _user_exists: # user already exists
            return Response({'message': 'Username already exists or email already used'}, status=status.HTTP_400_BAD_REQUEST) # return error response

        UserCredentials.objects.create(name=_username, password=_password, email=_email) # save user to database

        return Response({
            'name': _username,
            'password': _password,
        }, status=status.HTTP_201_CREATED) # return success response

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

        _user = UserCredentials.objects.filter(name=_username, password=_decrypted_password)
        if _user.exists() and _username != "assistant":
            return Response({
                "found": True
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "found": False
            }, status=status.HTTP_200_OK)

@api_view(['POST', 'GET'])
def assistant(_request):
    if _request.method == 'POST':
        _name = _request.data['assistant_name']
        _description = _request.data['description']
        _response_style = _request.data['response_style']
        _tone = _request.data['tone']
        _profile_picture = _request.data['profile_picture']
        _username = _request.data['username']
        _password = _request.data['password']

        _user = UserCredentials.objects.filter(name=_username, password=_password)

        if not _user.exists():
            return Response(
                {
                "message": "User not found"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        _assistant = Assistant.objects.create(
            name = _name,
            description = _description,
            response_style = _response_style,
            tone = _tone,
            profile_picture = _profile_picture
        )

        AssistantPermissions.objects.create(
            user = _user.get(),
            assistant = _assistant,
            can_edit = True,
            can_delete = True,
            can_view = True
        )

        return Response (
            {
                "assistant_id": _assistant.id
            },
            status=status.HTTP_201_CREATED
        )
    elif _request.method == 'GET':
        _username = _request.GET['username']
        _password = _request.GET['password']
        _user = UserCredentials.objects.filter(name=_username, password=_password)

        if not _user.exists():
            return Response(
                {
                    "message": "User not found"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        if "assistant_id" in _request.GET:
            _assistant_id = _request.GET["assistant_id"]
            _assistant = Assistant.objects.filter(id=_assistant_id)
            if not _assistant.exists():
                return Response(
                    {
                        "message": "Assistant not found"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            _assistant_permissions = AssistantPermissions.objects.filter(
                user=_user.get(),
                assistant=_assistant.get()
            )

            if not _assistant_permissions.exists() or not _assistant_permissions.get().can_view:
                return Response(
                    {
                        "message": "You do not have permission to view this assistant"
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )

            _assistant = _assistant.get()

            return Response(
                {
                    "assistant_id": _assistant.id,
                    "assistant_name": _assistant.name,
                    "description": _assistant.description,
                    "response_style": _assistant.response_style,
                    "tone": _assistant.tone,
                    "profile_picture": _assistant.profile_picture
                }, status=status.HTTP_200_OK
            )
        else:
            _username = _request.GET['username']
            _password = _request.GET['password']
            _user = UserCredentials.objects.filter(name=_username, password=_password)

            if not _user.exists():
                return Response(
                    {
                        "message": "User not found"
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )

            _permissions = AssistantPermissions.objects.filter(user=_user.get())

            _assistants = []

            for _permission in _permissions:
                _assistants.append({
                    "id": _permission.assistant.id,
                    "name": _permission.assistant.name,
                    "description": _permission.assistant.description,
                    "response_style": _permission.assistant.response_style,
                    "tone": _permission.assistant.tone,
                    "profile_picture": _permission.assistant.profile_picture
                })

            return Response(
                {
                    "assistants": _assistants
                },
                status=status.HTTP_200_OK
            )

@api_view(['POST', 'GET', 'PATCH'])
def conversation(_request):
    if _request.method == 'POST':
        _name = _request.data['conversation_name']
        _assistant_id = _request.data['assistant_id']
        _username = _request.data['username']
        _password = _request.data['password']

        _user = UserCredentials.objects.filter(name=_username, password=_password)
        if not _user.exists():
            return Response(
                {
                    "message": "User not found"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        _assistant = Assistant.objects.filter(id=_assistant_id)

        if not _assistant.exists():
            return Response(
                {
                    "message": "Assistant not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        _permissions = AssistantPermissions.objects.filter(user=_user.get(), assistant_id=_assistant.get(), can_edit = True)

        if not _permissions.exists():
            return Response(
                {
                    "message": "User does not have permission to create conversation"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        _conversation = Conversation.objects.create(
            name = _name,
            assistant = _assistant.get()
        )

        ConversationPermissions.objects.create(
            user = _user.get(),
            conversation = _conversation,
            can_edit = True,
            can_delete = True,
            can_view = True
        )

        return Response(
            {
                "conversation_id": _conversation.id
            },
            status=status.HTTP_201_CREATED
        )
    elif _request.method == 'GET':
        _username = _request.GET['username']
        _password = _request.GET['password']
        _user = UserCredentials.objects.filter(name=_username, password=_password)

        if not _user.exists():
            return Response(
                {
                    "message": "User not found"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        if "conversation_id" in _request.GET:
            _conversation_id = _request.GET["conversation_id"]
            _conversation = Conversation.objects.filter(id=_conversation_id)
            if not _conversation.exists():
                return Response(
                    {
                        "message": "Conversation not found"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            _conversation_permissions = ConversationPermissions.objects.filter(
                user=_user.get(),
                conversation=_conversation.get()
            )

            if not _conversation_permissions.exists() or not _conversation_permissions.get().can_view:
                return Response(
                    {
                        "message": "You do not have permission to view this assistant"
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )

            _conversation = _conversation.get()

            _conversation_messages = ConversationMessage.objects.filter(conversation=_conversation)

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
                            "sent_by_name": _message.sent_by.name,
                        } for _message in _conversation_messages
                    ]
                },
                status=status.HTTP_200_OK
            )
        else:
            _username = _request.GET['username']
            _password = _request.GET['password']
            _assistant_id = _request.GET['assistant_id']
            _user = UserCredentials.objects.filter(name=_username, password=_password)

            if not _user.exists():
                return Response(
                    {
                        "message": "User not found"
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )

            _assistant = Assistant.objects.filter(id=_assistant_id)

            _permissions = ConversationPermissions.objects.filter(user=_user.get(), can_view = True)

            _conversations = []

            for _permission in _permissions:
                if _permission.conversation.assistant.id == _assistant.get().id:
                    _conversations.append({
                        "id": _permission.conversation.id,
                        "name": _permission.conversation.name,
                        "date_of_creation": _permission.conversation.date_of_creation
                    })

            return Response(
                {
                    "conversations": _conversations
                },
                status=status.HTTP_200_OK
            )

@api_view(['POST'])
def message(_request):
    if _request.method == "POST":
        _message = _request.data['message']
        _conversation_id = _request.data['conversation_id']
        _username = _request.data['username']
        _password = _request.data['password']

        _user = UserCredentials.objects.filter(name=_username, password=_password)

        if not _user.exists():
            return Response(
                {
                    "message": "User not found"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        _conversation = Conversation.objects.filter(id=_conversation_id)
        if not _conversation.exists():
            return Response(
                {
                    "message": "Conversation not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        _conversation_permissions = ConversationPermissions.objects.filter(
            user=_user.get(),
            conversation=_conversation.get()
        )

        if not _conversation_permissions.exists() or not _conversation_permissions.get().can_edit:
            return Response(
                {
                    "message": "You do not have permission to edit this assistant"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        _conversation = _conversation.get()
        _assistant = _conversation.assistant

        ConversationMessage.objects.create(
            conversation=_conversation,
            message=_message,
            sent_by=_user.get(),
        )

        _conversation_messages = ConversationMessage.objects.filter(conversation=_conversation)

        _messages = [{
            "role": "system",
            "content": build_system_prompt(_assistant.description, _assistant.response_style, _assistant.tone)
        }]

        for _old_message in _conversation_messages:
            _messages.append({
                "role": "assistant" if _old_message.sent_by.id == 0 else "user",
                "content": _old_message.message
            })

        response = client.chat.completions.create(
            model="gpt-4-ai-model",
            messages=_messages,
        )

        ConversationMessage.objects.create(
            conversation=_conversation,
            message=response.choices[0].message.content,
            sent_by=UserCredentials.objects.filter(id=0).get(),
        )

        return Response({
            "message": response.choices[0].message.content
        }, status=status.HTTP_200_OK)

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