# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-19 06:20
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor_name', models.CharField(max_length=100)),
                ('ordered_by', models.CharField(max_length=100)),
                ('order_date', models.DateField()),
                ('delivery_address', models.CharField(max_length=200)),
                ('delivered', models.BooleanField(default=False)),
                ('delivered_on', models.DateField(auto_now_add=True)),
                ('charge', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Charge GH₵')),
                ('delivered_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('vendor_name',),
            },
        ),
    ]
