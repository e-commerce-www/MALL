from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, seller_status='default', **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, seller_status=seller_status, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, seller_status='approved', **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    SELLER_STATUS_CHOICES = (
        ('rejected', '거절됨'),
        ('default', '신청 안함'),
        ('pending', '대기중'),
        ('approved', '승인됨'),
    )
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    seller_status = models.CharField(max_length=15, choices=SELLER_STATUS_CHOICES, default='default')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email