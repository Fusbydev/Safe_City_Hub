from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
# Create your models here.

class Emergencies (models.Model):
    INCIDENT_TYPES = [
        ('crime', 'Crime'),
        ('accident', 'Accident'),
        ('civic', 'Civic'),
    ]
    
    URGENCY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    incident_type = models.CharField(max_length=20, choices=INCIDENT_TYPES)
    urgency_level = models.CharField(max_length=10, choices=URGENCY_LEVELS)
    date = models.DateTimeField()
    contact_number = models.CharField(max_length=20)
    description = models.TextField()
    proof = models.FileField(upload_to='proofs/', blank=True, null=True)
    anonymous = models.BooleanField(default=False)
    longitude = models.FloatField(default=0.0)
    latitude = models.FloatField(default=0.0)
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.description