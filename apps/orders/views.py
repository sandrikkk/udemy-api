from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.orders.serializers import OrderSerializer


class OrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        serializer = OrderSerializer(
            data=request.data, context={"request": request, "view": self}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
