from django.urls import path

from apps.orders import views

urlpatterns = [path("<int:pk>/orders", views.OrderAPIView.as_view(), name="orders")]
