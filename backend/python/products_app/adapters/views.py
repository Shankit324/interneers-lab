# adapters/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .repository import InMemoryProductRepository
from ..core.use_cases import ProductService

# Dependency Injection Global 
storage = InMemoryProductRepository()
service = ProductService(storage)

class ProductListCreateView(APIView):
    def post(self, request):
        try:
            product = service.create_product(request.data)
            return Response(product.__dict__, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        page = int(request.query_params.get('page', 1))
        products, total = service.list_products(page=page)
        return Response({
            "items": [p.__dict__ for p in products],
            "total": total,
            "page": page
        })
    
class ProductDetailView(APIView):
    def get(self, request, pk):
        """Fetch a single product"""
        try:
            product = service.get_product(pk)
            return Response(product)
        except LookupError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        """Update a product"""
        try:
            updated_product = service.update_product(pk, request.data)
            return Response(updated_product)
        except LookupError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Delete a product"""
        try:
            service.delete_product(pk)
            return Response(
                {"message": f"Product {pk} deleted successfully"}, 
                status=status.HTTP_204_NO_CONTENT
            )
        except LookupError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)