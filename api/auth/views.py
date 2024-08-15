from django.contrib.auth import authenticate, login
from django.shortcuts import render

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView, get_object_or_404, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from rest_registration.api.serializers import DefaultUserProfileSerializer

from account.models import User, UserResetPassword

# from api.auth.mixins import UltraModelViewSet
from api.auth.serializers import LoginSerializer, UserSerializer, RegisterUserSerializer, ProfileSerializer, \
    ChangePasswordSerializer, SendResetPasswordKeySerializer, ResetPasswordSerializer, GoogleAuth
from api.auth.services import ResetPasswordManager


def get_google_code(request):
    return render(request, 'index.html')


class GoogleAuthAPIView(GenericAPIView):
    serializer_class = GoogleAuth
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.get_or_create(user=user)[0]
        user_serializer = DefaultUserProfileSerializer(instance=user, context={'request': request})
        return Response({
            **user_serializer.data,
            'token': token.key,
        })


class LoginGenericAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(email=email, password=password)
        if user:
            token = Token.objects.get_or_create(user=user)[0]
            user_serializer = UserSerializer(instance=user, context={'request': request})
            return Response({
                **user_serializer.data,
                'token_key': token.key
            })
        return Response({'massage': 'Пользователь не найден или неверный пароль'},
                        status=status.HTTP_400_BAD_REQUEST)


class RegisterGenericApiView(GenericAPIView):
    serializer_class = RegisterUserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.get_or_create(user=user)[0]
        user_serializer = UserSerializer(instance=user, context={'request': request})
        return Response({
            **user_serializer.data,
            'token': token.key,
        })


class ProfileViewSet(ModelViewSet):
    queryset = User.objects.all()
    # pagination_class = SimpleResultPagination
    serializer_class = ProfileSerializer
    lookup_field = 'id'
    permission_classes = (AllowAny,)


class ChangePasswordApiView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (AllowAny,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if self.object.check_password(serializer.data.get("old_password")):
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Пароль успешно обновлен',
                    'data': []
                }

                return Response(response)
            else:
                return Response({"old_password": ['Неверный пароль']}, status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class SendResetPasswordKeyApiView(GenericAPIView):

    serializer_class = SendResetPasswordKeySerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email', None)
        user = get_object_or_404(User, email=email)
        if user:
            manager = ResetPasswordManager(user)
            manager.send_key()
            return Response({'detail': 'Ключ успещно отправлен'})
        return Response({'detail': 'пользователь с таким адресом электронной почты не существует'})


class ResetPasswordApiView(GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        key = serializer.validated_data.get('key', None)
        new_password = serializer.validated_data.get('new_password', None)
        user = get_object_or_404(UserResetPassword, key=key).user
        manager = ResetPasswordManager(user)
        is_changed = manager.reset_password(key, new_password)
        return Response(
            {'is_changed': is_changed},
            status=status.HTTP_200_OK if is_changed else status.HTTP_400_BAD_REQUEST
        )

