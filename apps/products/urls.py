from django.urls import path
from apps.products import views

urlpatterns = [
    path('', views.ProductList.as_view(), name="products"),
    path('<slug:category_slug>/<slug:product_slug>/', views.ProductDetail.as_view())
]
