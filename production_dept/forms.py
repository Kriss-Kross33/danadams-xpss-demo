from django import forms
from .models import MaterialsRequired, Product


class MaterialsRequiredInlineForms(forms.ModelForm):
    class Meta:
        model = MaterialsRequired
        fields = ['material', 'batch_no','material_code', 'quantity_required',
                  'quantity_issued', 'ar_no']



