from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password


class UserManager(BaseUserManager):
    """
    Custom user model manager.
    """
    def create_user(self, username, **extra_fields):
        """
        Create and save a user with the given extra fields.
        """
        if not username:
            raise ValueError(_('The Username field must be set'))
        user = self.model(username=username, **extra_fields)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        """
        Create and save a superuser with the given username and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        if not password:
            raise ValueError(_('The Password field must be set for superuser'))

        user = self.create_user(username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
        # return self.create_user(**extra_fields)
