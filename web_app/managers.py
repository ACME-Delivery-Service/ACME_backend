from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    @staticmethod
    def _validate_email(email):
        email_name, domain_part = email.strip().rsplit('@', 1)
        true_domain = settings.EMAIL_DOMAIN

        if true_domain and domain_part != true_domain:
            raise ValueError('Email has to be at `' + settings.EMAIL_DOMAIN + '` domain')

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('Email is required')

        email = self.normalize_email(email)
        self._validate_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        # extra_fields.setdefault('is_staff', False)
        # extra_fields.setdefault('is_superuser', False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        # extra_fields.setdefault('is_staff', True)
        # extra_fields.setdefault('is_superuser', True)

        # if extra_fields.get('is_staff') is not True:
        #     raise ValueError('Superuser must have is_staff=True.')
        # if extra_fields.get('is_superuser') is not True:
        #     raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
