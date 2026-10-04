from django.urls import path

from . import views

urlpatterns = [
    path("categories", views.CategoryListCreate.as_view(), name="category-list"),
    path("categories/<int:pk>", views.CategoryDetail.as_view(), name="category-detail"),
    path("products", views.ProductListCreate.as_view(), name="product-list"),
]
