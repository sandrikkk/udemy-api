from rest_framework.response import Response
from rest_framework.views import APIView

from apps.category.models import Category
from apps.category.serializers import CategorySerializer
from rest_framework.permissions import AllowAny


class CategoryApiView(APIView):
    queryset = Category.objects.all()
    permission_classes = [AllowAny]
    serializer_class = CategorySerializer

    def get(self, request):
        data = Category.objects.all()
        serializer = self.serializer_class(instance=data, many=True)
        return Response(data=serializer.data)
