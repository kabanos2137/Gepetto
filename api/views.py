from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from api.models import UserCredentials

@api_view(['POST'])
def create_account(request): # create_account view function
    if request.method == 'POST': # check if request method is POST
        username = request.data['username'] # get username from request
        password = request.data['password'] # get password from request
        email = request.data['email'] # get email from request

        user_exists = UserCredentials.objects.filter(name=username).exists() or UserCredentials.objects.filter(email=email).exists() # check if user already exists

        if user_exists: # user already exists
            return Response({'message': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST) # return error response

        UserCredentials.objects.create(name=username, password=password, email=email) # save user to database

        return Response({
            'name': username,
            'password': password,
        }, status=status.HTTP_201_CREATED) # return success response