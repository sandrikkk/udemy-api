from rest_framework import serializers

from apps.base.defaults import ProductDefault
from apps.orders.models import Order, Status


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    product = serializers.HiddenField(default=ProductDefault())
    status = serializers.HiddenField(default=Status.CANCELLED)

    class Meta:
        model = Order
        fields = ["user", "product", "status", "created_at", "updated_at"]

    def validate(self, attrs):
        attrs = super().validate(attrs)
        user = self.context["request"].user
        product = attrs.get("product")
        attrs["status"] = Status.SUCCEED
        if Order.objects.filter(
            user=user, product=product, status=Status.SUCCEED
        ).exists():
            raise serializers.ValidationError(
                "You have already made a order for this product."
            )
        return attrs

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["user"] = self.context["request"].user.id
        data["product"] = instance.product.name
        return data
