from apps.products.models import Product


class ProductDefault:
    requires_context = True

    def __call__(self, serializer_field):
        pk = serializer_field.context["view"].kwargs["pk"]
        return Product.objects.filter(id=pk).first()
