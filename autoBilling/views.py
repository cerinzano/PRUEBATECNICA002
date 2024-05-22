import json
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
import requests
from django.shortcuts import get_object_or_404, redirect, render
from .forms import JobSelectionForm, SelectionForm, ProductFormSet
from .models import Store, Persona, Product, Operation, Job

def select_items(request):
    if request.method == 'POST':
        print("POST")
        form = SelectionForm(request.POST)
        formset = ProductFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            response = request_availability (request)
            print(response.text)
            operation_id = createoperation(response.text)
            url = reverse('job_selection', kwargs={'operation_id': operation_id})
            # Redirigir a la URL construida
            return redirect(url)
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
        print("----->  Operation ID = ", operation.id)
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
    print("-----> Return  Operation ID = ", operation.id)
    return operation.id

def operation_list(request):
    operations = Operation.objects.prefetch_related('jobs').all()
    return render(request, 'autoBilling/operation_list.html', {'operations': operations})

def select_job(request, operation_id):
    operation = get_object_or_404(Operation, pk=operation_id)
    if request.method == 'POST':
        selected_job_id = request.POST.get('selected_job')
        selected_job = get_object_or_404(Job, pk=selected_job_id)
        return JsonResponse({
            'id_job': selected_job.id_job,
            'from_time': selected_job.from_time,
            'to_time': selected_job.to_time,
            'operational_model': selected_job.operational_model,
            'description': selected_job.description,
            'expires_at': selected_job.expires_at,
            'store_id': selected_job.store_id,
            'store_name': selected_job.store_name,
            'operation_id': selected_job.operation.id
        })
    return render(request, 'autoBilling/select_job.html', {'operation': operation})


def request_get_job(job_id):
    url = f"https://api.xandar.instaleap.io/jobs/{job_id}"
    headers = {
        "accept": "application/json",
        "x-api-key": "yoJYongi4V4m0S4LClubdyiu5nq6VIpxazcFaghi"
    }
    response = requests.get(url, headers=headers)
    return response

def job_detail(request, job_id):
    # URL del servicio web
    response = request_get_job(job_id)

    if response.status_code == 200:
        job_data = response.json()
        return render(request, 'autoBilling/job_detail.html', {'job': job_data})
    else:
        # Manejar el caso de error
        return render(request, 'autoBilling/job_detail.html', {'error': 'No se pudo obtener la información del Job.'})


def request_create_job (Job, Persona, Product):
    
    client_reference = str(Job.id) + "-" + Product.id_item
    print("client reference", client_reference)
    url = "https://api.xandar.instaleap.io/jobs"
    order_value = Product.price *  Product.quantity * 1.2
    payload = {
        "recipient": {
            "name": Persona.name,
            "email": "alvarez.dr@gmail.com",
            "phone_number": "3016088186"
        },
        "payment_info": {
            "prices": { "order_value": order_value},
            "payment": { "method": "CASH" },
            "currency_code": "COP"
        },
        "add_delivery_code": True,
        "contact_less": {
            "comment": "LeaveAtTheDoor",
            "cash_receiver": Persona.name,
            "phone_number": "3016088186"
        },
        "slot_id": Job.id_job,
        "client_reference": client_reference
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-api-key": "yoJYongi4V4m0S4LClubdyiu5nq6VIpxazcFaghi"
    }
    response = requests.post(url, json=payload, headers=headers)
    return response

def job_selection(request, operation_id):
    operation = get_object_or_404(Operation, id=operation_id)
    jobs = Job.objects.filter(operation=operation)
    personas = get_object_or_404(Persona, id=operation.persona.id)
    product = get_object_or_404(Product, id=operation.product.id)
    
    if request.method == 'POST':
        form = JobSelectionForm(request.POST, operation_id=operation_id)
        if form.is_valid():
            selected_job = form.cleaned_data['job']
            response = request_create_job (selected_job, personas, product)
            data = response.json()
            job_id = data.get('job_id')
            return redirect('job_detail', job_id=job_id)

            # Redirigir a la URL construida
            #return redirect(url)
            # return render(request, 'autoBilling/operation_success.html', {'response': response.json()})
        
        
    else:
        form = JobSelectionForm(operation_id=operation_id)
    return render(request, 'autoBilling/job_selection.html', {'operation': operation, 'form': form, 'jobs': jobs})



