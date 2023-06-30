from django.urls import path

from apps.reviews import views

urlpatterns = [
    path(
        "<int:pk>/reviews",
        views.Reviews.as_view(),
        name="reviews",
    )
]
