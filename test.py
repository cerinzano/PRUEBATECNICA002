import requests

url = "https://api.xandar.instaleap.io/jobs/availability/v2"

payload = {
    "origin": {
        "name": "Juan",
        "address": "Calle 112 # 18 12",
        "country": "Colombia",
        "city": "Bogotá",
        "state": "Bogota D.C.",
        "zip_code": "111211",
        "latitude": 4.697146,
        "longitude": -74.042459
    },
    "destination": {
        "name": "Pedro",
        "address": "Calle 118 # 12 40",
        "country": "Colombia",
        "city": "Bogotá",
        "state": "Cundinamarca",
        "zip_code": "111211",
        "latitude": 4.695228,
        "longitude": -74.047598
    },
    "operational_models_priority": ["FULL_SERVICE"],
    "job_items": [
        {
            "attributes": { "category": "Abarrotes" },
            "id": "12345",
            "name": "Arroz",
            "unit": "KG",
            "sub_unit": "LB",
            "quantity": 2,
            "sub_quantity": 1,
            "weight": 2,
            "volume": 2,
            "price": 2000,
            "comment": "Comentario"
        }
    ],
    "currency_code": "COP",
    "start": "2024-05-21T03:09:00.473318",
    "end": "2024-05-25T04:45:00.473318",
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

print(response.text)