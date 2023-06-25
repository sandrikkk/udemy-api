from django.urls import path

from apps.orders import views

urlpatterns = [path("<int:pk>/orders", views.OrderView.as_view(), name="Orders")]
