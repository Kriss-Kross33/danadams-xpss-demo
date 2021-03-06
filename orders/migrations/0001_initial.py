# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-19 06:20
from __future__ import unicode_literals

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor', models.CharField(max_length=50)),
                ('fullname', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('delivery_address', models.CharField(max_length=200)),
                ('contact_number', models.CharField(max_length=16, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{9,15}$')])),
                ('location', models.CharField(max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('paid', models.BooleanField(default=False)),
                ('ordered', models.BooleanField(default=True)),
                ('order_date', models.DateField(default=datetime.date.today)),
                ('payment_status', models.CharField(choices=[('PE', 'Pending'), ('AU', 'Authorized'), ('PA', 'Paid'), ('PR', 'Partially Refunded'), ('RE', 'Refunded'), ('VO', 'Void')], default='VO', max_length=2)),
            ],
            options={
                'ordering': ('vendor', '-created'),
                'permissions': (),
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Cost per unit')),
                ('date_arrived', models.DateField(blank=True, null=True)),
                ('serial', models.CharField(blank=True, max_length=45, null=True, verbose_name='Serial number')),
                ('location', models.CharField(blank=True, help_text='example: -80 freezer, refrigerator, Gilmer 283', max_length=45, null=True)),
                ('expiry_years', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True, verbose_name='Warranty or Item expiration (y)')),
                ('reconciled', models.BooleanField(default=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.Order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='inventory.Product')),
            ],
            options={
                'db_table': 'inventory_order_items',
            },
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('code', models.CharField(choices=[('CO', 'Cash On Delivery'), ('CH', 'Check / Money Order'), ('CC', 'Credit Card'), ('PO', 'Purchase Order'), ('MO', 'Mobile Money')], max_length=2, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('updated_by', models.CharField(max_length=100)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Payment Methods',
                'db_table': 'sales_payment_method',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.ForeignKey(db_column='payment_method_code', null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.PaymentMethod'),
        ),
        migrations.AddField(
            model_name='order',
            name='sales_person',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
