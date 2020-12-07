from django import forms
from .models import Order
# from suit.widgets import EnclosedInput


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['vendor', 'fullname', 'email', 'delivery_address', 'contact_number',
                  'location']

        widgets = {
            # By icons

        }

