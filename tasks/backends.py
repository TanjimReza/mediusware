# tasks/backends.py

from django.contrib.auth.backends import ModelBackend
from .models import TaskUser


class TaskUserAuthenticationBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = TaskUser.objects.get(email=email)
            if user.check_password(password):
                return user
        except TaskUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return TaskUser.objects.get(pk=user_id)
        except TaskUser.DoesNotExist:
            return None
