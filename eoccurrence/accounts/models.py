from django.db import models

import uuid

from django.contrib.auth.models import User

# Create your models here.
class Userprofile(models.Model):
    USER_ROLES = [
        ('public', 'Public'),
        ('police', 'Police Officer'),
        ('court', 'Court Official'),
        ('admin', 'System Admin'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    id_number = models.CharField(max_length=20, unique=True) # National ID or Police ID
    address = models.TextField(blank=True, null=True)
    user_role = models.CharField(max_length=50, choices=USER_ROLES, default='public')
    department = models.CharField(max_length=100, blank=True, null=True) # Police Dept or Court Dept
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    last_activity = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - ({self.user_role})"