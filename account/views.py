from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK
from .Serializers import UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework_jwt.settings import api_settings
import json
from .models import User


class RegistrationView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def create_user_objects(self, request):
        email = request.data.get('email')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        password = request.data.get('password')
        user = User(first_name=first_name, last_name=last_name, email=email)
        user.set_password(password)
        user.save()
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        response = {'token': token}
        response = json.dumps(response)
        response = json.loads(response)
        return response

    def post(self, request, *args, **kwargs):
        return Response((self.create_user_objects(request)), status=HTTP_200_OK)


class UsersListView(APIView):
    permission_class = IsAuthenticated
    serializer_class = UserSerializer

    def get_users_list(self, request):
        return User.objects.all()

    def get(self, request, *args, **kwargs):
        return Response(self.serializer_class(self.get_users_list(request), many=True).data, status=HTTP_200_OK)


class UserAvailibilityView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def get_check_availibility(self, request):
        user = User.objects.filter(email=request.data.get('email')).first()
        response = {'availability': True}
        if user:
            response["availability"] = False
        response = json.dumps(response)
        return json.loads(response)

    def post(self, request, *args, **kwargs):
        return Response(self.get_check_availibility(request), status=HTTP_200_OK)
