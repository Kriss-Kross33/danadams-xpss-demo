from django.db import models

class OrderManager(models.Manager):
    def get_queryset(self):
        return super(OrderManager, self).get_queryset(pk='pk')
