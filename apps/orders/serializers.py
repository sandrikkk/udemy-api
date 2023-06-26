from rest_framework import serializers

from apps.base.defaults import ProductDefault
from apps.orders.models import Order


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    product = serializers.HiddenField(default=ProductDefault())
    status = serializers.HiddenField(default=Order.STATUS[0][1])

    class Meta:
        model = Order
        fields = ["user", "product", "status", "created_at", "updated_at"]

    def validate(self, attrs):
        attrs = super().validate(attrs)
        user = self.context["request"].user
        product = attrs.get("product")
        attrs["status"] = Order.STATUS[0][0]
        if Order.objects.filter(
            user=user, product=product, status=Order.STATUS[0][0]
        ).exists():
            raise serializers.ValidationError(
                "You have already made a order for this product."
            )
        return attrs
