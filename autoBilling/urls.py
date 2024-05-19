from django.urls import path
from . import views

urlpatterns = [
    path('select-items/', views.select_items, name='select_items'),
]
