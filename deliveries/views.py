from django.shortcuts import render
from orders.models import Order
# Create your views here.


def delivery_order_list(request, user_id):
    order = Order.objects.filter()