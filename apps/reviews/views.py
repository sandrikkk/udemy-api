from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.products.models import Product
from apps.reviews.permissions import OrderPermission
from apps.reviews.serializer import ReviewSerializer


class Reviews(APIView):
    queryset = Product.objects.all()

    def get_permissions(self):
        if self.request.method == "GET":
            return [
                OrderPermission(),
            ]
        else:
            return [
                IsAuthenticated(),
            ]

    def get(self, request, pk):
        product = get_object_or_404(
            Product, id=pk
        )
        reviews = product.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        # This method handles the HTTP POST request.
        # However, it does not use the `category_slug` and `product_slug` parameters here it uses in review serializer.
        data = request.data
        serializer = ReviewSerializer(
            data=data, context={"request": request, "view": self}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
