from rest_framework import serializers

from apps.base.defaults import ProductDefault
from apps.orders.models import Order, Status


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    product = serializers.HiddenField(default=ProductDefault())
    status = serializers.HiddenField(default=Status.CANCELLED)

    class Meta:
        model = Order
        fields = ["id", "user", "product", "status", "created_at", "updated_at"]
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Order.objects.all(),
                fields=("product", "user"),
                message="You have already made an order for this product.",
            )
        ]

    def validate_user(self, user):
        if not user.is_verified:
            raise serializers.ValidationError("In order to make an order, your profile must first be verified.")
        return user

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["user"] = self.context["request"].user.id
        data["product"] = instance.product.name
        data["status"] = instance.status.name
        return data
