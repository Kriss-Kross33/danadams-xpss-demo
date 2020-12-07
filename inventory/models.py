# -*- coding: utf-8 -*-
# -*- mode: python -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.core.validators import RegexValidator
import datetime
from taggit.managers import TaggableManager

# TODO: Add sub-categories model


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    description = models.TextField(null=True, blank=True)
    pic = models.ImageField(upload_to='images/catalog/categories', null=True, blank=True)
    parent = models.ForeignKey('self', related_name='sub_categories', null=True, blank=True)
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_expended = models.BooleanField(default=False, help_text='Catergory will always shown expended')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ['name']

    def __init__(self, *args, **kwargs):
        super(Category, self).__init__(*args, **kwargs)
        self.sub_categories_list = None

    def __str__(self):
        if self.parent:
            return '%s > %s' % (self.parent, self.name)
        return self.name

    def get_all_sub_categories(self):
        """
        Returns all sub categories from children
        """
        for sub_category in self.sub_categories_list:
            yield sub_category
            # Returns children of sub categories
            for sub_category2 in sub_category.get_all_sub_categories():
                yield sub_category2

    def get_sub_categories(self, categories):
        sub_categories = []
        for sub_category in categories:
            if sub_category.parent_id == self.id:
                sub_category.parent = self
                sub_categories.append(sub_category)

        return sub_categories

    def get_absolute_url(self):
        return reverse('inventory:product_list_by_category',
                       args=[self.slug])


class Vendor(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=64, blank=True, null=True)
    lookup_url = models.CharField(max_length=128, blank=True, null=True,
                                  help_text="url pattern to look up catalog number")
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$')
    rep_phone = models.CharField(validators=[phone_regex], max_length=16)
    support_phone = models.CharField(validators=[phone_regex], max_length=16)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class ProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(available=True)


class Product(models.Model):
    name = models.CharField('Product Name', max_length=200, db_index=True)
    brand = models.CharField('Brand Name', max_length=200, db_index=True, blank=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to="products/%Y/%m/%d", blank=True)
    chem_formula = models.CharField('Chemical formula', max_length=45,
                                    blank=True, null=True)
    catalog = models.CharField('Catalog number', max_length=45,
                               blank=True, null=True)
    packaging = models.CharField(max_length=50, blank=True)
    manufacturer_number = models.CharField(max_length=45,
                                           blank=True, null=True)
    size = models.DecimalField('Size of unit',
                               max_digits=10, decimal_places=2,
                               blank=True, null=True)
    expiry = models.DateField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=9, decimal_places=2, default=0.0)
    cost = models.DecimalField(max_digits=9, decimal_places=2, default=0.0,
                               help_text='Per unit cost')
    sku = models.CharField(max_length=50, verbose_name='SKU', null=True, blank=True)
    delivery_cost = models.DecimalField(
        max_digits=9, decimal_places=2, default=0.0, help_text='Delivery cost per unit')
    stock = models.PositiveIntegerField()
    category = models.ForeignKey(Category)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    available = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    weight = models.FloatField(default=0)
    length = models.FloatField(default=0)
    width = models.FloatField(default=0)
    height = models.FloatField(default=0)
    is_bestseller = models.BooleanField(
        default=False, help_text='It has been best seller')
    is_featured = models.BooleanField(
        default=False, help_text='Promote this product on main pages')
    is_free_delivery = models.BooleanField(
        default=False, help_text='No shipping charges')
    objects = models.Manager()  # default manager
    availableProducts = ProductManager()   # custom  manager to get all the available products
    tags = TaggableManager()

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def unit_size(self):
        return "%s%s%s" % (self.size or "",
                           "" if str(self.unit).startswith("/") else " ",
                           self.unit)

    def total_price(self):
        return (self.cost or 0) * self.units_purchased

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

    def image_tag(self):
        if self.image:
            return u'<img src="%s" />' % self.image.url
        else:
            return '(No Image)'

    def get_absolute_url(self):
        return reverse('inventory:product_detail',
                       args=[self.id, self.slug])

    def get_discount(self):
        """
        Return discount on the product
        """
        if self.old_price:
            return int(((self.old_price - self.price) / self.old_price) * 100)

        return 0

    @classmethod
    def get_active(cls):
        return cls.objects.filter(available=True)

    @classmethod
    def featured_products(cls):
        """
        Returns featured products
        """
        return list(cls.get_active().filter(is_featured=True))

    @classmethod
    def featured_product_categories(cls, max_categories):
        """
        Returns the categories of the featured products
        :return:
        """
        return list(cls.objects.filter(available=True)[:max_categories])

    @classmethod
    def recent_products(cls, max_products):
        """
        Returns recent products arrivals
        """
        return list(cls.get_active().filter(available=True).order_by('-id')[:max_products])

    @classmethod
    def get_search(cls, q):
        """
        Returns QuerySet of product search query
        """
        return cls.get_active().filter(Q(name__icontains=q) |
                                       Q(category__name__icontains=q) |
                                       Q(brand__name__icontains=q) |
                                       Q(gist__icontains=q) |
                                       Q(tags__icontains=q))

    @classmethod
    def search_products(cls, q):
        """
        Returns products for search query
        """
        return cls.get_search(q)

    @classmethod
    def search_advance_products(cls, keyword, category, manufacturer, price_from, price_to, categories):
        """
        Returns list of products against search params
        """
        query = cls.get_search(keyword)

        if category:
            category = next(category2 for category2 in categories if category2.id == category.id)
            sub_categories_ids = [category.id]
            sub_categories_ids += (sub_category.id for sub_category in category.get_all_sub_categories())

            query = query.filter(category_id__in=sub_categories_ids)

        if manufacturer:
            query = query.filter(brand=manufacturer)
        if price_from:
            query = query.filter(price__gte=price_from)
        if price_to:
            query = query.filter(price__lte=price_to)

        return query

