from rest_framework.permissions import BasePermission

from apps.orders.models import Order, Status


class OrderPermission(BasePermission):
    def has_permission(self, request, view):
        order_status = Order.objects.filter(
            user=request.user, status=Status.SUCCEED
        ).first()
        # IF POST and not bought return False ELSE RETURN TRUe
        if request.method == "POST" and not order_status:
            return False
        return True
