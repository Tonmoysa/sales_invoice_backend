from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Extended User model with additional fields if needed"""
    email = models.EmailField(unique=True)
    
    class Meta:
        db_table = 'users'
        
    def __str__(self):
        return self.username


