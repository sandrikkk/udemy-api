from rest_framework import serializers
from apps.reviews.models import Review
from apps.orders.models import Order, STATUS


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['product', 'product', 'comment', 'star']

    def validate(self, attrs):
        request = self.context.get('request')
        product = attrs.get('product')

        user = request.user
        order = Order.objects.filter(user=user, product_id=product.id, status=STATUS[0][0]).first()

        if not order:
            raise serializers.ValidationError("You haven't purchased the associated product.")
        return attrs
