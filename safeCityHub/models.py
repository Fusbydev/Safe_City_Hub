from mongoengine import Document, StringField, DateTimeField, BooleanField, FloatField, FileField, IntField, ListField, EmbeddedDocument
from mongoengine.fields import GridFSProxy
import datetime
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
    submitted_at = DateTimeField(default=datetime.datetime.utcnow)
    address = StringField(max_length=200)
    status = StringField(choices=[('pending', 'Pending'), ('resolved', 'Resolved'), ('under_review', 'Under Review')], default='pending')
    ways_to_mitigate = StringField()
    comments = ListField(
        StringField(),
        default=[]
    )

    def __str__(self):
        return self.description
