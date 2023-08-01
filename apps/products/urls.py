from django.urls import path

from apps.products import views

urlpatterns = [
    path("", views.ProductListCreateView.as_view(), name="products"),
    path("<int:pk>/", views.ProductDetailView.as_view(), name="product-details"),
]
