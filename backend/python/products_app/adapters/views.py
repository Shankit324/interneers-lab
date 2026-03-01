# adapters/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from dataclasses import asdict  
from .repository import MongoProductRepository
from ..core.use_cases import ProductService

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