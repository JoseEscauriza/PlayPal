from django.contrib.auth.backends import ModelBackend

from .models import CustomUser


class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return None

        if user.check_password(password):
            return user

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None

