from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from .validators import PhoneValidator
from main.models import TimeStampedModel

class UserManager(BaseUserManager):

    def _create_user(self,phone,  email, password, **extra_fields):
        """
        Create and save a user with the given phone, email, and password.
        """
        if not phone:
            raise ValueError('The given phone must be set')
        email = self.normalize_email(email)
        # username = self.model.normalize_username(username)
        user = self.model(phone=phone, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone, email, password, **extra_fields)

    def create_superuser(self, phone, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone, email, password, **extra_fields)

BLOCKED_STATUS = ("1", "")

class User(AbstractUser):
    objects = UserManager()
    USERNAME_FIELD = "phone"
    phone = models.CharField(max_length=20, null=True, unique=True)#, validators=[PhoneValidator()])
    username = models.CharField(max_length=120, null=True)
    first_name = models.CharField(max_length=120)
    is_blocked = models.BooleanField(default=False)
    why_blocked = models.TextField(blank=True, null=True)
