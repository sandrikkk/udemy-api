from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.products.models import Product
from apps.reviews.models import Review
from apps.reviews.permissions import OrderPermission
from apps.reviews.serializer import ReviewSerializer
from rest_framework.permissions import IsAuthenticated


class Reviews(APIView):
    queryset = Product.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            return [OrderPermission(), ]
        else:
            return [IsAuthenticated(), ]

    def get(self, request, product_slug):
        product = Product.objects.filter(slug=product_slug).first()
        if not product:
            return Response({'detail': 'Product not Found'})

        reviews = product.reviews.all()
        if reviews:
            serializer = ReviewSerializer(reviews, many=True)
            return Response(serializer.data)
        else:
            return Response([], status=status.HTTP_200_OK)

    def post(self, request, product_slug):
        user = request.user
        data = request.data
        product = self.queryset.get(slug=product_slug)
        already_exist = product.reviews.filter(user=user).exists()

        if already_exist:
            content = {'details': 'Product has already reviewed'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        else:
            star = int(data['star'])
            Review.objects.create(
                user=user,
                product=product,
                star=star,
                comment=data['comment']
            )
            return Response("Review Added", status=status.HTTP_201_CREATED)
