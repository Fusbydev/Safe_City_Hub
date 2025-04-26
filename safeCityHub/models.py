from mongoengine import Document, ObjectIdField, StringField, DateTimeField, BooleanField, FloatField, FileField, IntField
import datetime
from django.contrib.auth.models import User

class Emergencies(Document):
    user = IntField(required=True)  # store Django's User.id (int)
    incident_type = StringField(choices=[('crime', 'Crime'), ('accident', 'Accident'), ('civic', 'Civic')], required=True)
    urgency_level = StringField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], required=True)
    date = DateTimeField(required=True)
    contact_number = StringField(max_length=20, required=True)
    description = StringField(required=True)
    proof = FileField(blank=True, null=True)
    anonymous = BooleanField(default=False)
    longitude = FloatField(default=0.0)
    latitude = FloatField(default=0.0)
    submitted_at = DateTimeField(default=datetime.datetime.utcnow)

    def __str__(self):
        return self.description
