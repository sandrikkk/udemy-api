from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.products.models import Product
from apps.products.paginations import CustomLimitOffsetPagination
from apps.products.permissions import CustomPermission
from apps.products.serializers import ProductSerializer


class ProductList(APIView):
    queryset = Product.objects.all()
    permission_classes = [CustomPermission]
    pagination_class = CustomLimitOffsetPagination

    def get(self, request):
        products = self._get_queryset(request)
        paginator = self.pagination_class()
        paginated_products = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(paginated_products, many=True)
        return paginator.get_paginated_response(serializer.data)

    def _get_queryset(self, request):
        if category_id := request.query_params.get("category"):
            return self.queryset.filter(category=category_id)

        return self.queryset

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductDetail(APIView):
    queryset = Product.objects.all()
    permission_classes = [CustomPermission]

    def get(self, request, pk):
        single_product = get_object_or_404(Product, id=pk)
        serializer = ProductSerializer(single_product, many=False)
        return Response(serializer.data)

    def put(self, request, pk):
        single_product = get_object_or_404(Product, id=pk)
        serializer = ProductSerializer(single_product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Object has been updated"})

    def delete(self, request, pk):
        single_product = get_object_or_404(Product, id=pk)
        single_product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
