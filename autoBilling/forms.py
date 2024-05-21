from datetime import timezone
from django import forms
from django.forms import ValidationError, formset_factory
from .models import Store, Persona, Product

class SelectionForm(forms.Form):
    destine = forms.ModelChoiceField(queryset=Persona.objects.all(), label='Destinatario')
    origin = forms.ModelChoiceField(queryset=Store.objects.all(), label='Origen')
    fecha_inicio = forms.DateTimeField(widget=forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'}))
    fecha_fin = forms.DateTimeField(widget=forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'}))

    # def clean_fecha_inicio(self):
    #     fecha_inicio = self.cleaned_data.get('fecha_inicio')
    #     if fecha_inicio <= timezone.now():
    #         raise ValidationError("La fecha de inicio debe ser posterior a la fecha actual.")
    #     return fecha_inicio

    # def clean_fecha_fin(self):
    #     fecha_fin = self.cleaned_data.get('fecha_fin')
    #     if fecha_fin <= timezone.now():
    #         raise ValidationError("La fecha de fin debe ser posterior a la fecha actual.")
    #     return fecha_fin

class ProductForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all(), label='Producto')
    quantity = forms.IntegerField(min_value=1, label='Cantidad')

ProductFormSet = formset_factory(ProductForm, extra=1)
