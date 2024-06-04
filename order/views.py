from .models import Order
from rest_framework import generics
from .serializer import OrderSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import ValidationError
from django.utils.translation import ugettext_lazy as _
from .tasks import send_purchase_confirmation  # Import the Celery task

class OrderView(generics.ListCreateAPIView):
    ''' API endpoint for order, just owner can access it '''
    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(client=user)

    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        if user.shopcart_item.all().count() == 0:
            raise ValidationError({"detail": _("Your cart is empty")})

        # Create the order
        order = self.create(request, *args, **kwargs).data

        # Trigger Celery task to send confirmation email (assuming order data is in 'order')
        send_purchase_confirmation.delay(user.email, order)

        return Response(order, status=status.HTTP_201_CREATED)  # Return created order data
