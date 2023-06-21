from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from apps.category.models import Category
from rest_framework.views import APIView
from apps.products.models import Product
from apps.products.serializer import ProductSerializer


class Categories(APIView):
    def get(self, request, category_slug):
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category)
        serializer = ProductSerializer(products, many=True)
        return Response({'Products': serializer.data})
