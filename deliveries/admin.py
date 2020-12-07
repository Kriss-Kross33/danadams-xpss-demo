from django.contrib import admin
from .models import Delivery
from orders.models import Order
# Register your models here.

"""
orders vendor, fullname, delivery_address, location, orderdate, delivered_date, delivered_by, ordered

"""


class DeliveryAdmin(admin.ModelAdmin):
    fields = ('order', 'vendor_name', 'ordered_by', 'order_date', 'delivery_address',
              'delivered_by', 'charge', 'delivered')
    list_display = ('vendor_name', 'ordered_by', 'order_date', 'delivered_on', 'delivery_address',
                    'delivered_by', 'charge', 'delivered')
    list_filter = ('delivered_by', 'delivered', 'delivered_on')
    list_editable = ('delivered',)
    search_fields = ('delivered_by',)
    raw_id_fields = ('delivered_by',)
admin.site.register(Delivery, DeliveryAdmin)
