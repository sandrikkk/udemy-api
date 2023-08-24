from rest_framework import serializers

from apps.base.defaults import ProductDefault
from apps.orders.models import Order, Status
from apps.reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    product = serializers.HiddenField(default=ProductDefault())

    class Meta:
        model = Review
        fields = ["product", "comment", "star", "user"]
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Review.objects.all(), fields=("product", "user"), message="Product has already been reviewed."
            )
        ]

    def validate_user(self, user):
        if not user.is_verified:
            raise serializers.ValidationError("In order to leave a review, your profile must first be verified.")
        return user

    def validate(self, attrs):
        attrs = super().validate(attrs)
        product = attrs.get("product")
        user = self.context.get("user")
        order = Order.objects.filter(user=user, product_id=product.id, status=Status.SUCCEED).first()
        if not order:
            raise serializers.ValidationError("You haven't purchased the associated product to review this product.")
        return attrs
