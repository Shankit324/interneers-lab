# products_app/apps.py
from django.apps import AppConfig
from django.conf import settings
import mongoengine
from datetime import datetime, timezone

class ProductsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products_app'

    def ready(self):
        try:
            mongoengine.connect(host=settings.MONGO_URI, alias='default')
            print("Connected to MongoDB.")
            
            # Run the Seed and Migration scripts on startup
            self.run_startup_migrations()
            
        except Exception as e:
            print(f"MongoDB Connection Error: {e}")

    def run_startup_migrations(self):
        """Seeds default categories and migrates legacy data."""
        # Get the raw PyMongo database object to bypass MongoEngine's strict validation during migration
        db = mongoengine.get_db()
        
        print("Running database migrations and seeding...")

        # --- 1. SEED DEFAULT CATEGORIES ---
        seed_categories = [
            {"title": "Food", "description": "Consumables and groceries"},
            {"title": "Kitchen Essentials", "description": "Cookware and utensils"},
            {"title": "Uncategorized", "description": "Default category for legacy items"}
        ]
        
        for cat in seed_categories:
            # Upsert: Insert if it doesn't exist
            db.product_categories.update_one(
                {"title": cat["title"]},
                {"$setOnInsert": {
                    "description": cat["description"],
                    "created_at": datetime.now(timezone.utc),
                    "updated_at": datetime.now(timezone.utc)
                }},
                upsert=True
            )

        # --- 2. MIGRATE OLD PRODUCTS (Handling string categories) ---
        # Find products where the 'category' field is still a string (BSON type 2)
        legacy_products = db.products.find({"category": {"$type": 2}})
        
        for prod in legacy_products:
            old_cat_name = prod.get("category")
            
            # Find or create a new Category Document for the old string
            cat_doc = db.product_categories.find_one({"title": old_cat_name})
            if not cat_doc:
                result = db.product_categories.insert_one({
                    "title": old_cat_name,
                    "description": f"Auto-migrated category",
                    "created_at": datetime.now(timezone.utc),
                    "updated_at": datetime.now(timezone.utc)
                })
                cat_id = result.inserted_id
            else:
                cat_id = cat_doc["_id"]
                
            # Update the product to use the new ObjectId reference instead of the string
            db.products.update_one({"_id": prod["_id"]}, {"$set": {"category": cat_id}})

        # --- 3. HANDLE MISSING BRANDS ---
        # Find any product that doesn't have a brand or has a null brand, and assign a default
        db.products.update_many(
            {"$or": [{"brand": {"$exists": False}}, {"brand": None}, {"brand": ""}]},
            {"$set": {"brand": "Legacy Unknown Brand"}}
        )

        print("Migrations complete!")