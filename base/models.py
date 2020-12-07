from django.db import models
import uuid

from river.models.fields.state import StateField
# Create your models here.


class Ticket(models.Model):
    ticket_num = models.CharField('Ticket Number', max_length=10, default=uuid.uuid4,
                                  editable=False)
    description = models.TextField()
    status = StateField(editable=False)

    def __str__(self):
        return "{}".format(self.ticket_num)

