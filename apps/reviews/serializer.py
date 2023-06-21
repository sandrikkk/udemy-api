from rest_framework import serializers, status
from rest_framework.response import Response

from apps.reviews.models import Review
from apps.orders.models import Order


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['product', 'product', 'comment', 'star']

    def validate(self, attrs):
        request = self.context.get('request')
        product = attrs.get('product')

        user = request.user
        order = Order.objects.filter(user=user, product_id=product.id, status='SUCCEED').first()

        if not order:
            raise serializers.ValidationError("You haven't purchased the associated product.")
        return attrs
