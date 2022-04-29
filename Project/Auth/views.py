# ------ rest framework imports -------
from django.http import response
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

# ------ models --------
from .models import User

from .serializers import (
    AccountSerializer,
)

# ------ django AUTH ------
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.password_validation import validate_password

class LoginAccount(APIView):
    permission_classes = (AllowAny,)

    serializer_class = AccountSerializer

    def post(self, request):
        email = (request.data.get("email",))
        password = request.data.get("password",)
        try:
            entered_usr = User.objects.get(email__iexact=email)
            if check_password(password,entered_usr.password ):
                return Response(message, status=status.HTTP_202_ACCEPTED)
            else:
                message = {'message':'Incorrect password'}
                return Response(message, status=status.HTTP_401_UNAUTHORIZED)
        except:
            message = {'message':'No matching user found'}
            return Response(message, status=status.HTTP_406_NOT_ACCEPTABLE)
        # check_pswd returns True for match
