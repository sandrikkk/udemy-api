from rest_framework import generics

from apps.products.models import Product
from apps.products.paginations import CustomLimitOffsetPagination
from apps.products.permissions import CustomPermission
from apps.products.serializers import ProductSerializer


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    permission_classes = [CustomPermission]
    pagination_class = CustomLimitOffsetPagination
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.query_params.get("category")
        if category_id:
            return queryset.filter(category=category_id)
        return queryset


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    permission_classes = [CustomPermission]
    serializer_class = ProductSerializer
