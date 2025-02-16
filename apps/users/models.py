from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser
from django.db.models import EmailField, BooleanField
from django.db.models import Model

from users.managers import CustomUserManager


class User(AbstractUser):
    username = None
    full_name = None
    email = EmailField(unique=True)
    is_active = BooleanField(default=False)
    # todo is_active true qib qoyish kerak avtamatik tasdiqlaganda
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
