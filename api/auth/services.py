from django.conf import settings
from django.core.mail import send_mail
from django.utils.html import format_html
from django.utils.html import strip_tags
# from django_rest_passwordreset.signals import reset_password_token_created
from rest_framework.generics import get_object_or_404

from account.models import UserResetPassword, User
from urllib.parse import urlencode


class ResetPasswordManager:

    def __init__(self, user):
        self.user = user
        print(type(self.user))
        self.payload = UserResetPassword.objects.get_or_create(user=self.user)[0]
        if self.payload.is_expired():
            self.payload.delete()
            self.payload = UserResetPassword.objects.get_or_create(user=self.user)[0]

    def _make_link(self):
        key = self.payload.key
        queries = urlencode({'key': key})
        front_host = settings.FRONT_HOST
        reset_password_link = settings.RESET_PASSWORD_LINK
        return f"{front_host}{reset_password_link}?{queries}"

    def send_key(self):
        link = self._make_link()
        # print(link)
        # key = self.payload.key
        subject, to, from_email = 'Сброс пароля | DramaTheatre.kg', self.user.email, settings.EMAIL_HOST_USER
        # html_message = format_html(f'<a href="{link}">это ссылка для сброса пароля</a>')
        # plain_message = strip_tags(html_message)
        html_message = f'это ссылка для сброса пароля: {link}'
        plain_message = strip_tags(html_message)

        send_mail(
            subject,
            plain_message,
            from_email,
            [to],
            html_message=plain_message
        )

    def reset_password(self, key: str, new_password: str) -> bool:
        real_key = self.payload.key
        user = self.user
        if real_key == key:
            user.set_password(new_password)
            user.save()
            self.payload.delete()
            return True
        return False