from mongoengine import (
    Document, StringField, DateTimeField, BooleanField, FloatField,
    FileField, IntField, ListField, EmbeddedDocument, EmbeddedDocumentField
)
from datetime import datetime
from django.contrib.auth.models import User
from django.db import models


class Profile_picture(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='profile_pictures/default.jpg')

    def __str__(self):
        return super().__str__()

class Comment(EmbeddedDocument):
    text = StringField(required=True)
    timestamp = DateTimeField(default=datetime.utcnow)


class Emergencies(Document):
    user = IntField(required=True)
    incident_type = StringField(choices=[('crime', 'Crime'), ('accident', 'Accident'), ('civic', 'Civic')], required=True)
    urgency_level = StringField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], required=True)
    date = DateTimeField(required=True)
    contact_number = StringField(max_length=20, required=True)
    description = StringField(required=True)
    proof = FileField(collection_name='proofs', required=False)
    anonymous = BooleanField(default=False)
    longitude = FloatField(default=0.0)
    latitude = FloatField(default=0.0)
    submitted_at = DateTimeField(default=datetime.utcnow)  # ✅ fixed here
    address = StringField(max_length=200)
    status = StringField(choices=[('pending', 'Pending'), ('resolved', 'Resolved'), ('under_review', 'Under Review')], default='pending')
    ways_to_mitigate = StringField()
    comments = ListField(EmbeddedDocumentField(Comment))

    def __str__(self):
        return self.description
