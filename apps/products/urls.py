from django.urls import path

from apps.products import views

urlpatterns = [
    path("", views.ProductListApiView.as_view(), name="products"),
    path("<int:pk>/", views.ProductDetailApiView.as_view()),
]
