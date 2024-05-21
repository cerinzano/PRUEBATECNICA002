from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from .forms import SelectionForm, ProductFormSet
from .models import Store, Persona, Product

def select_items(request):
    if request.method == 'POST':
        print("POST")
        form = SelectionForm(request.POST)
        formset = ProductFormSet(request.POST)
        if form.is_valid() and formset.is_valid():

            

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

# def request_Availability (request):
    
#     store = Store.objects.get(id=request.POST["origin"])
#     persona = Persona.objects.get(id=request.POST["destine"])
#     product = Product.objects.get(id=request.POST["form-0-product"])
#     quantity = int(request.POST["form-0-quantity"])
#     price = product.price * quantity
#     date_start = request.POST["fecha_inicio"]
#     date_end = request.POST["fecha_fin"]

#     url = "https://api.xandar.instaleap.io/jobs/availability/v2"
#     payload = {
#         "origin": {
#             "name": persona.name,
#             "address": persona.address,
#             "country": persona.country,
#             "city": persona.cy,
#             "state": "Bogota D.C.",
#             "zip_code": "111211",
#             "latitude": 4.697146,
#             "longitude": -74.042459
#         },
#         "destination": {
#             "name": "Pedro",
#             "address": "Calle 118 # 12 40",
#             "country": "Colombia",
#             "city": "Bogotá",
#             "state": "Cundinamarca",
#             "zip_code": "111211",
#             "latitude": 4.695228,
#             "longitude": -74.047598
#         },
#         "operational_models_priority": ["FULL_SERVICE"],
#         "job_items": [
#             {
#                 "attributes": { "category": "Abarrotes" },
#                 "id": "12345",
#                 "name": "Arroz",
#                 "unit": "KG",
#                 "sub_unit": "LB",
#                 "quantity": 2,
#                 "sub_quantity": 1,
#                 "weight": 2,
#                 "volume": 2,
#                 "price": 2000,
#                 "comment": "Comentario"
#             }
#         ],
#         "currency_code": "COP",
#         "start": "2024-05-21T03:09:00.473318",
#         "end": "2024-05-25T04:45:00.473318",
#         "slot_size": 60,
#         "fallback": True,
#         "store_reference": "101_FS"
#         }
#     headers = {
#         "accept": "application/json",
#         "content-type": "application/json",
#         "x-api-key": "yoJYongi4V4m0S4LClubdyiu5nq6VIpxazcFaghi"
#     }

# response = requests.post(url, json=payload, headers=headers)