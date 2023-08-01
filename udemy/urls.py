from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

SWAGGER = [
    path("products/", include("apps.orders.urls")),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc')
]
urlpatterns = [
                  path("admin/", admin.site.urls),
                  path("api-auth/", include("rest_framework.urls")),
                  path("products/", include("apps.products.urls")),
                  path("user/", include("apps.users.urls")),
                  path("products/", include("apps.reviews.urls")),
                  # path("categories/", include("apps.category.urls")),
              ] + SWAGGER
