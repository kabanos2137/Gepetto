from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from setuptools.command.bdist_egg import can_scan

from api.models import UserCredentials, Assistant, AssistantPermissions


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
        print(_request.data) # print request data for debugging
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

@api_view(['GET'])
def login(_request):
    if _request.method == 'GET':
        _username = _request.GET['username']
        _password = _request.GET['password']
        _user = UserCredentials.objects.filter(name=_username, password=_password)
        if _user.exists():
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
        print(_request.data)
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

