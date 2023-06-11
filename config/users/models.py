from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
#from django.contrib.auth import get_user_model

from .manager import CustomUserManager

#UserModel = get_user_model() # получение всей модели пользователей


class CustomUser(AbstractUser):
    avatar = models.ImageField()
    email = models.EmailField(_("email address"), unique=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email