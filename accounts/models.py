from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.


class GuestEmail(models.Model):
    email = models.EmailField()
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class UserManager(BaseUserManager):
    def create_user(self, email, full_name=None, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError('User must have an email address.')
        if not password:
            raise ValueError('User must have a password.')
        user_obj = self.model(
            email=self.normalize_email(email), full_name=full_name)
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.is_active = is_active
        user_obj.admin = is_admin
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, password=None):
        user = self.create_user(email, password=password, is_staff=True)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password=password,
                                is_staff=True, is_admin=True)
        return user


class User(AbstractBaseUser):
    full_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'

    objects = UserManager()

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    @property
    def is_staff(self):
        if self.is_admin:
            return True
        return self.staff

    @property
    def is_admin(self):
        return self.admin
        
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True