from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin
)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """Creates and saves new user with email\
         instead of using username"""
        if not email:
            return ValueError(
                _('Every user must have an email address'))

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    @property
    def user_profile_picture(self):
        try:
            return self.profile.profile_picture.url
        except Exception as e:
            return None


class UserInfo(models.Model):
    user = models.OneToOneField(
        User, related_name='profile', on_delete=models.CASCADE,
        blank=True, null=True)
    bio = models.CharField(max_length=255, blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to='profiles', blank=True, null=True)

    def __str__(self):
        return "{}'s profile".format(str(self.user))
