
from django.forms import ModelForm
from django.forms import inlineformset_factory
from .models import Shipment, ShipmentItem


class ShipmentForm(ModelForm):
    items = inlineformset_factory(
        Shipment, ShipmentItem,
        fields=['name', 'quantity'], can_delete=False)

    class Meta:
        model = Shipment
        fields = [
            'shipment_no', 'first_name', 'last_name',
            'email', 'phone', 'address', 'zipcode',
            'city', 'state', 'country'
        ]
