from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser
from django.db.models import EmailField, BooleanField
from django.db.models import Model, CharField

from users.managers import CustomUserManager


class User(AbstractUser):
    username = None
    first_name = None
    last_name = None
    email = EmailField(unique=True)
    name = CharField(max_length=255)
    is_active = BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
