from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from django.urls import path
from apps.users import views

from apps.users.views import LoginUser

urlpatterns = [
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('registration/', views.RegisterUser.as_view(), name='registration'),
    path('login/', LoginUser.as_view(), name='login'),
    path('profile/', views.GetUserProfile.as_view())
]

