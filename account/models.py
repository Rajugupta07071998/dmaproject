from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('personal', 'Personal'),
        ('business', 'Business'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15, unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'mobile_number']

    def get_full_name(self):
        """Returns the full name of the user"""
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name if full_name else self.username  # Agar first_name ya last_name na ho, toh username return kare

    def __str__(self):
        return self.get_full_name() 
