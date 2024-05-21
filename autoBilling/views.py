import json
from django.db import transaction
from django.http import HttpResponse, JsonResponse
import requests
from django.shortcuts import get_object_or_404, render
from .forms import SelectionForm, ProductFormSet
from .models import Store, Persona, Product, Operation, Job

# def option_list(request):
#     options = Option.objects.all()
#     return render(request, 'option_list.html', {'options': options})

def operation_list(request):
    return HttpResponse('No options selected')
    # if request.method == 'POST':
        # selected_options = {}
        # for operation in Operation.objects.all():
        #     selected_option_id = request.POST.get(f'selected_option_{operation.id}')
        #     if selected_option_id:
        #         selected_options[operation.id] = selected_option_id
        # if selected_options:
        #     return HttpResponse(f'Selected Options: {selected_options}')
        # else:
            # return HttpResponse('No options selected')

    # operations = Operation.objects.all().prefetch_related('options')
    # return render(request, 'autoBilling/operation_list.html', {'operations': operations})


def select_items(request):
    if request.method == 'POST':
        print("POST")
        form = SelectionForm(request.POST)
        formset = ProductFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            response = request_availability (request)
            print(response.text)
            createoperation(response.text)
            # print("--------------------------")
            # print(store.address)
            # print(persona)
            # print(product)
            # print(quantity)
            # print(price)
            # print(date_start)
            # print(date_end)
            # print("--------------------------")
            # store = get_object_or_404(Store, id=store_id)
            # Process the valid form data here
            # store = Store.objects.get(name = request.POST["origin"])
            # print (store.address)
            return render(request, 'autoBilling/selection_success.html', {'form': form, 'formset': formset})
    else:
        print("Other")
        form = SelectionForm()
        formset = ProductFormSet()
    return render(request, 'autoBilling/select_items.html', {'form': form, 'formset': formset})

def request_availability (request):
    
    store = Store.objects.get(id=request.POST["origin"])
    persona = Persona.objects.get(id=request.POST["destine"])
    product = Product.objects.get(id=request.POST["form-0-product"])
    quantity = int(request.POST["form-0-quantity"])
    price = product.price * quantity
    date_start = request.POST["fecha_inicio"]
    date_end = request.POST["fecha_fin"]

    url = "https://api.xandar.instaleap.io/jobs/availability/v2"
    payload = {
        "origin": {
            "name": store.name,
            "address": store.address,
            "country": store.country,
            "city": store.city,
            "state": store.state,
            "zip_code": store.zip_code,
            "latitude": store.latitude,
            "longitude": store.longitude
        },
        "destination": {
            "name": persona.name,
            "address": persona.address,
            "country": persona.country,
            "city": persona.city,
            "state": persona.state,
            "zip_code": persona.zip_code,
            "latitude": persona.latitude,
            "longitude": persona.longitude
        },
        "operational_models_priority": ["FULL_SERVICE"],
        "job_items": [
            {
                "attributes": { "category": "Bicicletas" },
                "id": product.id_item,
                "name": product.name,
                "unit": product.unit,
                "sub_unit": product.sub_unit,
                "quantity": quantity,
                "sub_quantity": 1,
                "weight": product.weight * quantity,
                "volume": product.volume * quantity,
                "price": price,
                "comment":product.comment
            }
        ],
        "currency_code": "COP",
        "start": date_start,
        "end": date_end,
        "slot_size": 60,
        "fallback": True,
        "store_reference": "101_FS"
        }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-api-key": "yoJYongi4V4m0S4LClubdyiu5nq6VIpxazcFaghi"
    }
    response = requests.post(url, json=payload, headers=headers)
    return response

def createoperation(obj_operation):
    
    data = json.loads(obj_operation)
    
    with transaction.atomic():

        operation = Operation.objects.create()
        for item in data:
            # Crear o actualizar el registro de StoreAvailable
            # Crear el registro de Job
            job = Job.objects.create(
                id_job=item['id'],
                from_time=item['from'],
                to_time=item['to'],
                operational_model=item['operational_model'],
                description=item['description'],
                expires_at=item['expires_at'],
                store_id=item['store']['id'],
                store_name=item['store']['name'],
                operation=operation
            )


