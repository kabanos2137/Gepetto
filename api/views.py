from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from api.models import UserCredentials

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
        _name = _request.data['assistant_name']
        _description = _request.data['description']
        _response_style = _request.data['response_style']
        _tone = _request.data['tone']
        _profile_picture = _request.data['profile_picture']
        _username = _request.data['username']
        _password = _request.data['password']

        return Response(
            {},
            status=status.HTTP_201_CREATED
        )