from rest_framework import serializers

from apps.products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "created_at",
            "updated_at",
            "deleted",
            "name",
            "description",
            "price",
            "images",
            "category",
        ]
