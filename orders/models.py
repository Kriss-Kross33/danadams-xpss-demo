from django.db import models
from django.core.validators import RegexValidator
from django.core.urlresolvers import reverse
from inventory.models import Product
from django.contrib.auth.models import User
import datetime
from django.conf import settings
# Create your models here.


class OrderManager(models.Manager):
    def get_queryset(self):
        return super(OrderManager, self).get_queryset().filter(id='id', ordered=True)


class PaymentMethod(models.Model):
    """
    Represents payment methods for order
    """
    # Payment methods
    COD = 'CO'
    CHECK = 'CH'
    CREDIT_CARD = 'CC'
    PURCHASE_ORDER = 'PO'
    MOBILE_MONEY = 'MO'
    ALL = ((COD, 'Cash On Delivery'),
           (CHECK, 'Check / Money Order'),
           (CREDIT_CARD, 'Credit Card'),
           (PURCHASE_ORDER, 'Purchase Order'),
           (MOBILE_MONEY, 'Mobile Money'))
    ALL_METHODS = dict(ALL)

    code = models.CharField(primary_key=True, max_length=2, choices=ALL)
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    updated_by = models.CharField(max_length=100)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)

    class Meta:
        db_table = 'sales_payment_method'
        verbose_name_plural = 'Payment Methods'

    def __str__(self):
        return '%s: %s' % (self.code, self.name)

    @classmethod
    def get_all(cls):
        """
        Returns list of active/supported payments method
        """
        return list(cls.objects.filter(is_active=True))


class Order(models.Model):
    # Payment statuses
    PAYMENT_PENDING = 'PE'
    PAYMENT_AUTHORIZED = 'AU'
    PAYMENT_PAID = 'PA'
    PAYMENT_PARTIALLY_REFUNDED = 'PR'
    PAYMENT_REFUNDED = 'RE'
    PAYMENT_VOID = 'VO'
    PAYMENT_STATUSES = ((PAYMENT_PENDING, 'Pending'),
                        (PAYMENT_AUTHORIZED, 'Authorized'),
                        (PAYMENT_PAID, 'Paid'),
                        (PAYMENT_PARTIALLY_REFUNDED, 'Partially Refunded'),
                        (PAYMENT_REFUNDED, 'Refunded'),
                        (PAYMENT_VOID, 'Void'))
    vendor = models.CharField(max_length=50)
    fullname = models.CharField(max_length=100)
    email = models.EmailField()
    delivery_address = models.CharField(max_length=200)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$')
    contact_number = models.CharField(validators=[phone_regex], max_length=16)  # validators should be a list
    location = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    ordered = models.BooleanField(default=True)
    order_date = models.DateField(default=datetime.date.today)
    sales_person = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, null=True,
                                     limit_choices_to={'is_staff': True})
    payment_method = models.ForeignKey(PaymentMethod, db_column='payment_method_code', null=True)
    payment_status = models.CharField(max_length=2, choices=PAYMENT_STATUSES, default=PAYMENT_VOID)
    objects = models.Manager()  # The default manager.
    order_manager = OrderManager()  # Our custom manager.

    class Meta:
        ordering = ('vendor', '-created',)
        permissions = (

        )

    def __str__(self):
        if self.ordered:
            status = self.order_date
        else:
            status = "in progress"
        return 'Order {0} {1} {2}'.format(self.id, self.fullname, status)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    @property
    def item_count(self):
        return self.items.count

    def get_full_address(self):
        return "{0}, {1}".format(self.delivery_address, self.location)

    def get_payment_status(self):
        return next((status[1] for status in self.PAYMENT_STATUSES if status[0] == self.payment_status), None)

"""
    def save(self, *args, **kwargs):
        users = User.objects.filter(groups__name='Sales Person')
        for user in users:
            if self.sales_person == user:
                super(Order, self).save(*args, **kwargs)
"""


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items')
    product = models.ForeignKey(Product, related_name='products')
    quantity = models.IntegerField(default=1)
    price = models.DecimalField('Cost per unit', max_digits=10, decimal_places=2,
                               blank=True, null=True)
    date_arrived = models.DateField(blank=True, null=True)
    serial = models.CharField('Serial number', max_length=45,
                              blank=True, null=True)
    location = models.CharField(max_length=45, blank=True, null=True,
                                help_text="example: -80 freezer, refrigerator, Gilmer 283")

    expiry_years = models.DecimalField('Warranty or Item expiration (y)', max_digits=4,
                                       decimal_places=2, blank=True, null=True)

    reconciled = models.BooleanField(default=True)

    class Meta:
        db_table = "inventory_order_items"

    def get_cost(self):
        if self.price is None:
            return 0
        else:
            return self.price * self.quantity

    def name(self):
        return self.product.name

    def order_date(self):
        return self.order.order_date

    def __str__(self):
        return '{0} {1} {2}'.format(self.id, self.product.name, self.order.order_date)


def vendor_url(self):
    try:
        return self.vendor.lookup_url % self.catalog
    except (AttributeError, TypeError):
        return None


def mfg_url(self):
    try:
        return self.manufacturer.lookup_url % self.manufacturer_number
    except (AttributeError, TypeError):
        return None


