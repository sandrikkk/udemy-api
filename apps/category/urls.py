from django.urls import path
from apps.category import views

urlpatterns = [
    path('<str:category_slug>/', views.Categories.as_view())
]
