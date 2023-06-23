from django.urls import path

from apps.category import views

urlpatterns = [path("<slug:category_slug>/", views.Categories.as_view())]
