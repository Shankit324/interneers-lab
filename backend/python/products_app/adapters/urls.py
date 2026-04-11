# products_app/adapters/urls.py
from django.urls import path
from .views import (
    ProductListCreateView, 
    ProductDetailView,
    ProductCategoryView,        # New: CRUD for Categories
    CategoryProductListView,    # New: Products by Category
    ProductBulkUploadView       # New: CSV Bulk Upload
)

urlpatterns = [
    # New endpoint for Bulk Upload (Requirement 6)
    path('products/bulk-upload/', ProductBulkUploadView.as_view(), name='product-bulk-upload'),

    # Existing endpoints
    path('products/', ProductListCreateView.as_view(), name='product-list'),
    path('products/<str:pk>/', ProductDetailView.as_view(), name='product-detail'),
    
    # New endpoints for Category Management (Requirement 3 & 4)
    path('categories/', ProductCategoryView.as_view(), name='category-list'),
    path('categories/<str:cat_id>/products/', CategoryProductListView.as_view(), name='category-products'),
    
]