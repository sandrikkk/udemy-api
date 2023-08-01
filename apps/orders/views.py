from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.orders.models import Order
from apps.orders.serializers import OrderSerializer


class OrderAPIView(CreateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [
        IsAuthenticated,
    ]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["pk"] = self.kwargs.get("pk")
        return context
