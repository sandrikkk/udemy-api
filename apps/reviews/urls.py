from django.urls import path

from apps.reviews import views

urlpatterns = [
    path(
        "<slug:category_slug>/<slug:product_slug>/reviews",
        views.Reviews.as_view(),
        name="Reviews",
    )
]
