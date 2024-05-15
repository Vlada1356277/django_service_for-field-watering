from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password


class UserManager(BaseUserManager):
    """
    Custom user model manager.
    """
    def create_user(self, **extra_fields):
        """
        Create and save a user with the given extra fields.
        """
        user = self.model(**extra_fields)
        user.save(using=self._db)
        return user

    def create_superuser(self, password, **extra_fields):
        """
        custom super_user'
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        user = self.model(password=make_password(password), **extra_fields)
        user.save(using=self._db)
        return user
        # return self.create_user(**extra_fields)
