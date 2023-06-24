from rest_framework import serializers

from apps.orders.models import STATUS, Order
from apps.products.models import Product
from apps.reviews.models import Review


class ProductDefault:
    requires_context = True

    def __call__(self, serializer_field):
        pk = serializer_field.context["view"].kwargs["pk"]
        return Product.objects.filter(
            id=pk
        ).first()


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    product = serializers.HiddenField(default=ProductDefault())

    class Meta:
        model = Review
        fields = ["product", "comment", "star", "user"]

    def validate(self, attrs):
        attrs = super().validate(attrs)
        request = self.context.get("request")
        product = attrs.get("product")
        user = request.user
        order = Order.objects.filter(
            user=user, product_id=product.id, status=STATUS[0][0]
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
