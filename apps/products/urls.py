from django.urls import path
from apps.products import views

urlpatterns = [
    path('', views.ProductList.as_view(), name="products"),
    path('<int:pk>/', views.ProductDetail.as_view())
]
