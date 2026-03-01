# products_app/models.py
from mongoengine import Document, StringField, FloatField, IntField, DateTimeField
from datetime import datetime, timezone

class ProductDocument(Document):
    meta = {'collection': 'products'} # Name of the collection in MongoDB
    
    name = StringField(required=True, max_length=255)
    description = StringField()
    category = StringField(max_length=100)
    price = FloatField(required=True)
    brand = StringField(max_length=100)
    quantity = IntField(default=0)
    
    # Audit Columns
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    updated_at = DateTimeField(default=lambda: datetime.now(timezone.utc))

    def save(self, *args, **kwargs):
        # Simply update the timestamp every time the document is saved.
        # MongoEngine automatically preserves the original 'created_at' date.
        self.updated_at = datetime.now(timezone.utc)
        return super().save(*args, **kwargs)