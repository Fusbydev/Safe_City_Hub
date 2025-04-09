from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
# Create your models here.

class Emergencies (models.Model):
    incident_type = models.CharField(max_length=255)
    urgency_level = models.CharField(max_length=255)
    date_time = models.DateTimeField()
    contact_number = models.CharField(max_length=255)
    description = models.TextField()
    proof = models.FileField(upload_to='proofs/')
    anonymous = models.BooleanField(default=True)
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title