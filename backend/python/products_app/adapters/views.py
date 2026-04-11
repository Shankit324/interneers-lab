# adapters/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from dataclasses import asdict  
from .repository import MongoProductRepository
from ..core.use_cases import ProductService, ProductCategoryService

storage = MongoProductRepository()
service = ProductService(storage)

class ProductListCreateView(APIView):
    def post(self, request):
        product = service.create_product(request.data)
        return Response(asdict(product), status=status.HTTP_201_CREATED)
        
    def get(self, request):
        products, total = service.list_products() # (We will add pagination here soon)
        return Response({"items": [asdict(p) for p in products], "total": total})

class ProductDetailView(APIView):
    def get(self, request, pk):
        try:
            product = service.get_product(pk)
            return Response(asdict(product))
        except LookupError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            updated_product = service.update_product(pk, request.data)
            return Response(asdict(updated_product))
        except LookupError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
            
    def delete(self, request, pk):
        try:
            service.delete_product(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except LookupError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        
from .repository import MongoCategoryRepository # Ensure you implement this in repository.py
cat_storage = MongoCategoryRepository()
cat_service = ProductCategoryService(cat_storage, storage)

class ProductCategoryView(APIView):
    def post(self, request):
        """Requirement 3: Add a new category"""
        category = cat_service.create_category(
            title=request.data.get('title'),
            description=request.data.get('description')
        )
        return Response(asdict(category), status=status.HTTP_201_CREATED)

    def get(self, request):
        """Requirement: List all categories (to verify seeding)"""
        categories = cat_service.list_all_categories() # Add this method to your service
        return Response([asdict(c) for c in categories])

class CategoryProductListView(APIView):
    def get(self, request, cat_id):
        """Requirement 3a: Fetch list of products in a category"""
        products = cat_service.get_products_in_category(cat_id)
        return Response([asdict(p) for p in products])

class ProductBulkUploadView(APIView):
    parser_classes = [MultiPartParser] # Required for file uploads

    def post(self, request, *args, **kwargs):
        
        if 'file' not in request.FILES:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
            
        file = request.FILES['file']
        try:
            content = file.read().decode('utf-8')
            # service is the instance of ProductService initialized in the file
            service.bulk_create_from_csv(content) 
            return Response({"status": "success"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(f"DEBUG Error: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)