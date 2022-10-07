from django.db import models
from django.contrib.auth.models import  AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class CustomUserManager(BaseUserManager):
    def create_user(self,email,password,**extra_fields):
        if not email:
            raise ValueError('Users must have an email address.')
        email = self.normalize_email(email)
        new_user = self.model(email =email,**extra_fields)
        new_user.set_password(password)
        new_user.save()
        return new_user

    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Super user should have is_staff be True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('SuperUser should have is_superuser be True')

        super_user =  self.create_user(email,password,**extra_fields)
        return super_user


# Create custom model
class CustomUser(AbstractUser):
    username = models.CharField(max_length=10,unique=True)
    email = models.EmailField(max_length=80,unique=True)
    phone_number = PhoneNumberField(null=False,unique = True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','phone_number']
    objects = CustomUserManager()

    def __str__(self):
        return f"<User {self.email}"



