from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('products/', include('apps.products.urls')),
    path('user/', include('apps.users.urls')),
    path('products/', include('apps.reviews.urls')),
    path('categories/', include('apps.category.urls'))
]

