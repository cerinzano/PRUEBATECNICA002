from django.shortcuts import render
from .forms import SelectionForm, ProductFormSet

def select_items(request):
    if request.method == 'POST':
        form = SelectionForm(request.POST)
        formset = ProductFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            # Process the valid form data here
            return render(request, 'autoBilling/selection_success.html', {'form': form, 'formset': formset})
    else:
        form = SelectionForm()
        formset = ProductFormSet()
    return render(request, 'autoBilling/select_items.html', {'form': form, 'formset': formset})
