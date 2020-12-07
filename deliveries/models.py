from django.db import models
from django.contrib.auth.models import User
from inventory.models import Product, Vendor, Category
from orders.models import Order
from django.conf import settings
# Create your models here.


class Delivery(models.Model):
    order = models.ForeignKey(Order)
    vendor_name = models.CharField(max_length=100)
    ordered_by = models.CharField(max_length=100)
    order_date = models.DateField()
    delivery_address = models.CharField(max_length=200)
    delivered_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, null=True)
    delivered = models.BooleanField(default=False)
    delivered_on = models.DateField(auto_now_add=True)
    charge = models.DecimalField('Charge GH₵', max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.vendor_name = self.order.vendor
        self.delivery_address = self.order.get_full_address()
        self.ordered_by = self.order.fullname
        self.delivered_by = self.order.sales_person
        self.order_date = self.order.order_date
        self.charge = self.order.get_total_cost()

        super(Delivery, self).save(*args, **kwargs)

    class Meta:
        ordering = ('vendor_name',)

    def __str__(self):
        if self.delivered:
            status = self.order_date
        else:
            status = "in progress"
        return "%s (%s)" % (self.vendor_name, status)


