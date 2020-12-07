from django.db import models
from django.core.validators import RegexValidator
from river.models.fields.state import StateField
from django.contrib.auth.models import User
# Create your models here.


class Manufacturer(models.Model):
    name = models.CharField(max_length=64)
    url = models.CharField(max_length=64, blank=True, null=True)
    lookup_url = models.CharField(max_length=64, blank=True, null=True,
                                  help_text="url pattern to look up part number")
    # rep = models.CharField(max_length=128, blank=True, null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$')
    phone = models.CharField(validators=[phone_regex], max_length=16)
    support_phone = models.CharField(validators=[phone_regex], max_length=16, blank=True)
    location = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_manufacturer_details(self):
        return "{0} {1} {2}".format(self.name, self.address, self.location)

    class Meta:
        ordering = ['name']


class Material(models.Model):
    product_name = models.CharField('Product', max_length=100)
    order_number = models.CharField('Order No', max_length=20, unique=True)
    gra_num = models.CharField('GRA No', max_length=20, unique=True)
    manufacturer = models.ForeignKey('Manufacturer', on_delete=models.CASCADE)
    chem_formula = models.CharField('Chemical formula', max_length=45,
                                    blank=True, null=True)
    description = models.TextField(blank=True)
    date_arrived = models.DateField()
    manufacture_date = models.DateField()
    expiry_date = models.DateField()
    weight = models.PositiveIntegerField('Weight(kg)')
    unit_price = models.DecimalField('Unit Price(GH₵)', max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    recieved_note = models.ForeignKey('ReceivedNote', on_delete=models.CASCADE, related_name='receivednote',
                                      null=True)
    recieved_advice_note = models.ForeignKey('ReceivedAdviceNote', on_delete=models.CASCADE,
                                             related_name='receivedadvicenote', null=True)

    class Meta:
        ordering = ('product_name',)

    def __str__(self):
        return '{0}'.format(self.product_name)

    def get_total(self):
        if self.unit_price is None:
            return 0
        else:
            return self.unit_price * self.quantity


class ReceivedNote(Material):
    # prepared_by = None
    # approved_by = None
    batch_no = models.CharField(max_length=25, unique=True)
    date_prepared = models.DateField(blank=True, null=True)
    stock_received = models.PositiveIntegerField(blank=True)
    approved = models.BooleanField(default=False)
    remarks = models.CharField(max_length=50, blank=True)
    status = StateField(editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('batch_no',)


class ReceivedAdviceNote(models.Model):
    batch_no = models.CharField(max_length=25, unique=True)
    prepared_on = models.DateField(blank=True, null=True)
    status = StateField(editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)

    class Meta:
        ordering = ('batch_no',)




