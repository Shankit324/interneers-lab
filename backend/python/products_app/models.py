# products_app/models.py
from mongoengine import Document, StringField, FloatField, IntField, DateTimeField, ReferenceField
from datetime import datetime, timezone

class ProductCategoryDocument(Document):
    meta = {'collection': 'product_categories'}
    
    title = StringField(required=True, unique=True, max_length=100)
    description = StringField()
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    updated_at = DateTimeField(default=lambda: datetime.now(timezone.utc))

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now(timezone.utc)
        return super().save(*args, **kwargs)

class ProductDocument(Document):
    meta = {'collection': 'products'}
    
    name = StringField(required=True, max_length=255)
    description = StringField()
    # Link to the Category Document
    category = ReferenceField(ProductCategoryDocument, required=False) 
    price = FloatField(required=True)
    # Brand is now explicitly required at the database level
    brand = StringField(required=True, max_length=100) 
    quantity = IntField(default=0)
    
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    updated_at = DateTimeField(default=lambda: datetime.now(timezone.utc))

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now(timezone.utc)
        return super().save(*args, **kwargs)