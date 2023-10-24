from django.db.models import Q

from django.contrib.auth import get_user_model

from django.contrib.auth.backends import ModelBackend


user = get_user_model()

class UsernameAndEmailBackend(object):
    def authenticate(self, username=None, password=None, **kwargs):
       email = kwargs.get('email')
       if email is None or username is None:
            return None
       try:
            user = MyUser.objects.get(username=username, email=email)
            if user.check_password(password):
                return user
       except MyUser.DoesNotExist:
            return None




class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(account_number=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None




from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User


class UE(object):
    def authenticate(self, request, username=None, password=None):
        UserModel = get_user_model()
        
        login_valid = UserModel.account_number == username
        
        if login_valid:
            try:
                user = User.objects.get(account_number=username)
            except User.DoesNotExist:
                return None
            else:
                if user.check_password(password):
                    return user
            
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None