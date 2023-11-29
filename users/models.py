from django.contrib.auth.models import AbstractUser
from django.db import models

from courses.models import NULLABLE


class User(AbstractUser):
    username = None  # удаляем поле username, так как авторизовать будем по полю email
    email = models.EmailField(unique=True, verbose_name='Email')

    phone = models.CharField(max_length=35, verbose_name='Phone number', **NULLABLE)
    city = models.CharField(max_length=50, verbose_name='City', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='Avatar', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ('email',)
