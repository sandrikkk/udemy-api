from apps.reviews import views
from django.urls import path

urlpatterns = [
    path('<slug:product_slug>/reviews', views.Reviews.as_view(), name="Reviews")
]
