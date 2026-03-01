# products_app/apps.py
from django.apps import AppConfig
from django.conf import settings
import mongoengine

class ProductsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products_app'

    def ready(self):
        # Pass the secure URI from your settings into MongoEngine
        try:
            mongoengine.connect(host=settings.MONGO_URI, alias='default')
            print("Successfully connected to secure MongoDB via MongoEngine!")
        except Exception as e:
            print(f"Failed to connect to MongoDB: {e}")