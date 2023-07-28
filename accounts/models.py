from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# For creating a user upon signup
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# User should have store
from inventory.models import Store



class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        # Username is required
        if not username:
            raise ValueError('The username field is required')
        # Email is also required
        if not email:
            raise ValueError('Please enter your email address')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)



# The User model
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='stores', null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # To avoid the conflict of User default name
    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        related_name='myuser_set',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        related_name='myuser_set',
        related_query_name='user',
    )

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f"{self.username} - {self.email}"

