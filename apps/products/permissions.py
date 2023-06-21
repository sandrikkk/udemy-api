from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission


class CustomPermission(BasePermission):
    def get_permissions(self):
        if self == 'GET':
            return [AllowAny()]
        else:
            return [IsAuthenticated()]

