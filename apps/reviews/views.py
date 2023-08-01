from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView
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
        product = get_object_or_404(Product, id=pk)
        reviews = product.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        pk = self.kwargs["pk"]
        serializer = ReviewSerializer(
            data=request.data,
            context={"request": request, "pk": pk, "user": request.user},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
# class OrderAPIView(CreateAPIView):
#     serializer_class = ReviewSerializer
#     queryset = Product.objects.all()
#     permission_classes = [
#         IsAuthenticated,
#     ]
# 
#     def get_permissions(self):
#         if self.request.method == "GET":
#             return [
#                 OrderPermission(),
#             ]
#         else:
#             return [
#                 IsAuthenticated(),
#             ]
# 
#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         context["pk"] = self.kwargs.get("pk")
#         context['user']
#         return context
