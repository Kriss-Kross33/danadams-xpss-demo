# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-19 06:20
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('pic', models.ImageField(blank=True, null=True, upload_to='images/catalog/categories')),
                ('display_order', models.IntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('is_expended', models.BooleanField(default=False, help_text='Catergory will always shown expended')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_categories', to='inventory.Category')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200, verbose_name='Product Name')),
                ('brand', models.CharField(blank=True, db_index=True, max_length=200, verbose_name='Brand Name')),
                ('slug', models.SlugField(max_length=200)),
                ('image', models.ImageField(blank=True, upload_to='products/%Y/%m/%d')),
                ('chem_formula', models.CharField(blank=True, max_length=45, null=True, verbose_name='Chemical formula')),
                ('catalog', models.CharField(blank=True, max_length=45, null=True, verbose_name='Catalog number')),
                ('packaging', models.CharField(blank=True, max_length=50)),
                ('manufacturer_number', models.CharField(blank=True, max_length=45, null=True)),
                ('size', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Size of unit')),
                ('expiry', models.DateField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('old_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('cost', models.DecimalField(decimal_places=2, default=0.0, help_text='Per unit cost', max_digits=9)),
                ('sku', models.CharField(blank=True, max_length=50, null=True, verbose_name='SKU')),
                ('delivery_cost', models.DecimalField(decimal_places=2, default=0.0, help_text='Delivery cost per unit', max_digits=9)),
                ('stock', models.PositiveIntegerField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('available', models.BooleanField(default=True)),
                ('description', models.TextField(blank=True)),
                ('weight', models.FloatField(default=0)),
                ('length', models.FloatField(default=0)),
                ('width', models.FloatField(default=0)),
                ('height', models.FloatField(default=0)),
                ('is_bestseller', models.BooleanField(default=False, help_text='It has been best seller')),
                ('is_featured', models.BooleanField(default=False, help_text='Promote this product on main pages')),
                ('is_free_delivery', models.BooleanField(default=False, help_text='No shipping charges')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Category')),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('url', models.CharField(blank=True, max_length=64, null=True)),
                ('lookup_url', models.CharField(blank=True, help_text='url pattern to look up catalog number', max_length=128, null=True)),
                ('rep_phone', models.CharField(max_length=16, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{9,15}$')])),
                ('support_phone', models.CharField(max_length=16, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{9,15}$')])),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AlterIndexTogether(
            name='product',
            index_together=set([('id', 'slug')]),
        ),
    ]
