from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, get_user_model
from django.conf import settings

from google.oauth2 import id_token
from google.auth.transport import requests

from account.models import User
from api.serializers import CartSerializer


class GoogleAuth(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.CharField()

    def create(self, validated_data):
        try:
            tooken = id_token.verify_oauth2_token(
                validated_data['token'], requests.Request(), settings.GOOGLE_OAUTH2_CLIENT_ID
            )
        except Exception as e:
            raise ValueError('Bad token Google')

        user, _ = User.objects.get_or_create(email=validated_data['email'])
        user.first_name = tooken['name'],
        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_login',
        )


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(validators=[validate_password])

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'password'
        )
        extra_kwargs = {
            'first_name': {'required': True},
        }

    def validate(self, attrs):
        for item in attrs.items():
            if not item[1]:
                raise ValidationError({
                    item[0]: [
                        f'{item[0]} не может быть пустым'
                    ]
                })
        return attrs

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    old_password = serializers.CharField(required=True,)
    new_password = serializers.CharField(required=True, validators=[validate_password])


# class CartForUserHistorySerializer(serializers.ModelSerializer):
#     model = Cart
#     fields = ()


class ProfileSerializer(serializers.ModelSerializer):
    carts = CartSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'password', 'carts')

    def validate(self, attrs):
        for item in attrs.items():
            if not item[1]:
                raise ValidationError({
                    item[0]: [
                        f'{item[0]} не может быть пустым'
                    ]
                })
        return attrs

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class SendResetPasswordKeySerializer(serializers.Serializer):

    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):

    key = serializers.UUIDField()
    new_password = serializers.CharField(validators=[validate_password])
