from django.db import models
from raw_materials_dept.models import Material, Manufacturer
from river.models.fields.state import StateField
# Create your models here.


class BatchNumber(models.Model):
    number = models.CharField(max_length=20, unique=True)

    class Meta:
        ordering = ('number',)

    def __str__(self):
        return "{}".format(self.number)


class Product(models.Model):
    name = models.CharField(max_length=100)
    batch_no = models.CharField(max_length=25, unique=True)
    batch_size = models.PositiveIntegerField('Batch Size (kg)', blank=True)
    manufacture_date = models.DateField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = StateField(editable=False)

    class Meta:
        ordering = ('batch_no', 'name')
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name


class MaterialsRequired(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    material = models.CharField('Material Name', max_length=100)
    material_code = models.CharField(max_length=25, unique=True)
    quantity_required = models.PositiveIntegerField('Qty Issued (kg)')
    quantity_issued = models.PositiveIntegerField('Qty Required (kg)')
    ar_no = models.CharField('A.R No', max_length=25, unique=True)
    batch_no = models.CharField(max_length=25, unique=True, blank=True)

    class Meta:
        ordering = ('material',)

    def __str__(self):
        return '{0} {1}'.format(self.batch_no, self.material)


class GoodsTransferNote(Product):
    class Meta:
        proxy = True
        ordering = ('batch_no',)
