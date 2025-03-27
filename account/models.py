from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
#from attendance.models import *


class User(AbstractUser):
    """
    Custom User model extending AbstractUser.

    Attributes:
        - `id` (UUIDField): Primary key for the user model.
        - `email` (EmailField): Unique email address.
        - `mobile_number` (CharField): Unique mobile number.
        - `user_type` (CharField): Defines the type of user (Personal/Business).
        - `master_policy` (ForeignKey): References a MasterPolicy.
        - `batch_policy` (ForeignKey): References a Batch.
    """

    USER_TYPE_CHOICES = (
        ('personal', 'Personal'),
        ('business', 'Business'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15, unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    is_private = models.BooleanField(default=False)

     # Lazy Reference से Circular Import Fix
    master_policy = models.ForeignKey(
        'attendance.MasterPolicy',  # String Reference
        on_delete=models.SET_NULL, blank=True, null=True, related_name="users_master_policy"
    )
    batch_policy = models.ForeignKey(
        'attendance.Batch',  # String Reference
        on_delete=models.SET_NULL, blank=True, null=True, related_name="users_batch_policy"
    )


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'mobile_number']

    def get_full_name(self):
        """Returns the full name of the user"""
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name if full_name else self.username  # Agar first_name ya last_name na ho, toh username return kare

    def __str__(self):
        return self.get_full_name() 
