from apps.orders.models import Order, STATUS
from rest_framework import serializers


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def validate(self, attrs):
        user = self.context['request'].user
        product = attrs['product']
        if Order.objects.filter(user=user, product=product, status=STATUS[0][0]).exists():
            raise serializers.ValidationError("You have already made a free order for this product.")

        return attrs
