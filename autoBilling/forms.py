from django import forms
from django.forms import formset_factory
from .models import Store, Persona, Product

class SelectionForm(forms.Form):
    destine = forms.ModelChoiceField(queryset=Persona.objects.all(), label='Destinatario')
    origin = forms.ModelChoiceField(queryset=Store.objects.all(), label='Origen')

class ProductForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all(), label='Producto')
    quantity = forms.IntegerField(min_value=1, label='Cantidad')

ProductFormSet = formset_factory(ProductForm, extra=1)
