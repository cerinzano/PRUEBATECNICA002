from django.urls import path
from . import views

urlpatterns = [
    path('select-items/', views.select_items, name='select_items'),
    path('operations/', views.operation_list, name='operation_list'),
    path('operations/<int:operation_id>/select_job/', views.select_job, name='select_job'),

]