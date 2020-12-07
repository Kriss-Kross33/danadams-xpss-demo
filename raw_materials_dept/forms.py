from django import forms
from .models import Material, ReceivedNote, ReceivedAdviceNote
from django.forms.models import BaseInlineFormSet


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['product_name', 'manufacturer', 'order_number', 'gra_num', 'chem_formula',
                  'date_arrived', 'description', 'manufacture_date', 'expiry_date', 'weight',
                  'quantity', 'unit_price',]


class MaterialInlineFormset(BaseInlineFormSet):
    def save_new_objects(self, commit=True):
        saved_instances = super(MaterialInlineFormset, self).save_new_objects(commit)
        if commit:
        # create book for press
            pass
        return saved_instances

    def save_existing_objects(self, commit=True):
        saved_instances = super(MaterialInlineFormset, self).save_existing_objects(commit)
        if commit:
            pass
        # update book for press
        return saved_instances

class GoodsReceivedNoteForm(forms.ModelForm):
    class Meta:
        model = ReceivedNote
        fields = ['batch_no', 'stock_received', 'approved', 'remarks']



# class GoodsReceivedNoteFormset()
