from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    # Setup createuser with custom fields. The manager handles authentication so this tells it what to expect from out CustomUser as far as unique fields.
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The email address you entered is invalid')
        
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        # override the default permissions
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        # creating a user with the overridden permissions
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(unique=True, max_length=50)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    
    REQUIRED_FIELDS = []

    # This is the name that will show up in the admin screen
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


    def __str__(self):
        return self.email
