from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from apps.products.models import Product
from apps.products.permissions import CustomPermission
from apps.products.serializer import ProductSerializer
from rest_framework.response import Response


class ProductList(APIView):
    queryset = Product.objects.all()
    permission_classes = [CustomPermission]

    def get(self, request):
        products = self.queryset.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=201)


class ProductDetail(APIView):
    queryset = Product.objects.all()
    permission_classes = [CustomPermission]

    def get(self, request, category_slug, product_slug):
        single_product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)
        serializer = ProductSerializer(single_product, many=False)
        return Response(serializer.data)

    def put(self, request, product_slug):
        single_product = get_object_or_404(Product, slug=product_slug)
        serializer = ProductSerializer(single_product,
                                       data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Object has been updated"})

    def delete(self, request, product_slug):
        single_product = get_object_or_404(Product, slug=product_slug)
        single_product.delete()
        return Response({"message": "Object has been deleted"}, status=status.HTTP_204_NO_CONTENT)
