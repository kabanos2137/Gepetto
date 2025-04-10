# api/decorators.py

from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED

from .models import UserCredentials, UserTokens

def require_auth(view_func):
    def wrapper(request, *args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Token "):
            return Response(
                {
                    "message": "Unauthorized access",
                    "action": "REDIR_TO_LOGIN"
                },
                status=HTTP_401_UNAUTHORIZED
            )

        token = auth_header.replace("Token ", "")
        try:
            user_tokens = UserTokens.objects.get(token=token)
            user = user_tokens.user
        except UserTokens.DoesNotExist:
            return Response(
                {
                    "message": "Token is invalid",
                    "action": "REDIR_TO_LOGIN"
                },
                status=HTTP_401_UNAUTHORIZED
            )

        request.user = user
        return view_func(request, *args, **kwargs)
    return wrapper