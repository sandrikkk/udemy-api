from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.orders.models import Order, Status
from apps.orders.serializers import OrderSerializer
from apps.orders.tasks import send_order_completion_email
from apps.products.models import Product


class OrderAPIView(CreateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [
        IsAuthenticated,
    ]

    def perform_create(self, serializer):
        super().perform_create(serializer)

        order = serializer.instance

        order.status = Status.SUCCEED

        order.save()
        send_order_completion_email.delay(order.user.email)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["pk"] = self.kwargs.get("pk")
        return context
