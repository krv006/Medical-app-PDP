from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser
from django.db.models import EmailField, BooleanField
from django.db.models import Model
from django.db.models.fields import CharField

from users.managers import CustomUserManager


class User(AbstractUser):
    username = None
    full_name = None
    phone_number = CharField(max_length=20, null=True, blank=True)
    email = EmailField(unique=True)
    is_active = BooleanField(default=False)
    # todo is_active true qib qoyish kerak avtamatik tasdiqlaganda
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
