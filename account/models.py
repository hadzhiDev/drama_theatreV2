import random
from uuid import uuid4

from django.contrib.auth.models import Permission
from django.contrib.auth.models import Group
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

from utils.models import TimeStampAbstractModel

from .managers import UserManager


class User(AbstractUser, TimeStampAbstractModel):
    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ('-date_joined',)

    username = None
    email = models.EmailField(verbose_name='электронная почта', unique=True, blank=False, null=False)
    groups = models.ManyToManyField(Group, related_name='account_users')
    user_permissions = models.ManyToManyField(Permission, related_name='account_users_permissions')

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{str(self.email) or self.first_name}'


def get_expire_date():
    return timezone.now() + timezone.timedelta(minutes=15)


def random_num():
    return int(''.join(random.choices('0123456789', k=4)))


class UserResetPassword(TimeStampAbstractModel):
    class Meta:
        verbose_name = 'Ключ для сброса пароля'
        verbose_name_plural = 'Ключи для сброса пароля'
        ordering = ('-created_at', '-updated_at')

    user = models.OneToOneField('account.User', on_delete=models.CASCADE, verbose_name='пользователь',
                                related_name='key')
    key = models.UUIDField('ключ', default=uuid4, editable=False, unique=True)
    expire_date = models.DateTimeField('срок действия', default=get_expire_date)

    def __str__(self):
        return f'{self.user}'

    def is_expired(self):
        return timezone.now() > self.expire_date
