from rest_framework import serializers

from apps.orders.models import STATUS, Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["user", "product", "user", "status", "created_at", "updated_at"]

    def validate(self, attrs):
        attrs = super().validate(attrs)
        user = self.context["request"].user
        product = attrs.get("product")
        if Order.objects.filter(
            user=user, product=product, status=STATUS[0][0]
        ).exists():
            raise serializers.ValidationError(
                "You have already made a order for this product."
            )

        return attrs
