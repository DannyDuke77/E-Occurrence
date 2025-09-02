from django.db import models

import uuid

# Create your models here.
from django.db import models

class SupportRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('resolved', 'Resolved'),
    ]

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Support request from {self.name} ({self.email})"
    
    # Set name = "Anonymous" if not provided
    def save(self, *args, **kwargs):
        if not self.name:
            self.name = "Anonymous"
        super().save(*args, **kwargs)