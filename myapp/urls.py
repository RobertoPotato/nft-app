from django.contrib import admin
from django.urls import path
from . import views

app_name = 'myapp'
urlpatterns = [
    path('', views.index),
    path('products', views.products),
    path('products/<str:contract_address>/<str:contract_name>/<int:contract_num_sales>', views.product_details, name='product_details'),
    path('contract/<str:contract_address>', views.contract, name='contract'), 
    path('address/', views.address_transactions, name='address'), 
]
