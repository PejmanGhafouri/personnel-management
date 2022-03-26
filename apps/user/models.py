import uuid

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from safedelete import SOFT_DELETE


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, national_id, password, **extra_fields):
        if not national_id:
            raise ValueError(_('The given national id must be set'))
        self.national_id = national_id
        user = self.model(national_id=national_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, national_id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(national_id, password, **extra_fields)

    def create_superuser(self, national_id, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self._create_user(national_id, password, **extra_fields)


# TODO (pejman) check django softdelete package support for user
class User(AbstractUser):
    _safedelete_policy = SOFT_DELETE

    username = None
    national_id = models.CharField(
        max_length=11,
        db_index=True,
        unique=True,
        validators=[RegexValidator(regex=r'^[0-9]\d{9}$|^[1-9]\d{10}$', message=_('invalid national id'))],
        verbose_name=_('National id'),
    )
    email = models.EmailField(  # This field needed to be replaced to make it 'unique = True'
        unique=True,
        verbose_name=_('Email Address'),
        error_messages={
            'unique': _('A user with this email already exists'),
        },
    )
    phone_number = models.CharField(
        max_length=13,
        db_index=True,
        unique=True,
        validators=[RegexValidator(regex=r'^\+\d{1,3}\d{10}$', message=_('invalid phone number'))],
        verbose_name=_('Phone Number'),
    )

    def __str__(self):
        return self.get_full_name()

    class Meta:
        ordering = ('first_name', 'last_name')
        get_latest_by = 'date_joined'
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    USERNAME_FIELD = 'national_id'
    objects = UserManager()
