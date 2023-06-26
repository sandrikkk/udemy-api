from rest_framework import serializers

from apps.base.defaults import ProductDefault
from apps.orders.models import Order
from apps.reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    product = serializers.HiddenField(default=ProductDefault())

    class Meta:
        model = Review
        fields = ["product", "comment", "star", "user"]

    def validate(self, attrs):
        attrs = super().validate(attrs)
        product = attrs.get("product")
        user = self.context.get("user")
        order = Order.objects.filter(
            user=user, product_id=product.id, status=Order.STATUS[0][0]
        ).first()
        if not order:
            raise serializers.ValidationError(
                "You haven't purchased the associated product to review this product."
            )
        already_exist = product.reviews.filter(user=user).exists()
        if already_exist:
            raise serializers.ValidationError(
                {"detail": "Product has already been reviewed."}
            )
        return attrs
