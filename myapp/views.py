from multiprocessing import context
from django.shortcuts import render
from django.http import HttpResponse
from .models import Product
import requests

CO2_PER_TRANSACTION = 40
CO2_FOR_MINTING = 18

def index(request):

    # Get assets for a certain address
    if request.method == 'POST':
        address = request.POST.get('search')
        total_sales = 0
        
        url = f"https://testnets-api.opensea.io/api/v1/assets?owner={address}&order_direction=desc&offset=0&limit=20&include_orders=false"

        response = requests.get(url).json()

        assets_list = response['assets']
        for asset in assets_list:
            sales = asset['num_sales']
            total_sales += int(sales)

        sales_carbon = total_sales * CO2_PER_TRANSACTION

        context = {
            "search_address": address,
            "total_assets": len(response['assets']),
            "total_sales": total_sales,
            "sales_carbon": sales_carbon,
            "minting_carbon": CO2_FOR_MINTING,
            "total_carbon": CO2_FOR_MINTING + sales_carbon
        }

        return render(request, 'myapp/address_consumption.html', context)

    else:
        url_get_assets = "https://testnets-api.opensea.io/api/v1/assets?order_by=sale_count&order_direction=desc&offset=0&limit=50&include_orders=true"

        response = requests.get(url_get_assets).json()

        return render(request, 'myapp/index.html', {"response": response['assets']})


def products(request):
    products = Product.objects.all()

    context = {"products": products}

    return render(request, 'myapp/index.html', context)


def product_details(request, contract_address, contract_name, contract_num_sales):
    
    print(f"contract address is : {contract_address}")

    sales = contract_num_sales * CO2_PER_TRANSACTION

    context = {
        "name": contract_name,
        "minting": CO2_FOR_MINTING,
        "sales_count": contract_num_sales,
        "total_sales": sales,
        "total": (contract_num_sales * CO2_PER_TRANSACTION) + CO2_FOR_MINTING

    }

    return render(request, 'myapp/detail.html', context)


def contract(request, contract_address):

    url = f"https://testnets-api.opensea.io/api/v1/asset_contract/{contract_address}"

    response = requests.get(url).json()

    context = {
        "contract": response["collection"]
    }

    return render(request, 'myapp/contracts.html', context)


def asset_events(request, account_address):

    url = f"https://testnets-api.opensea.io/api/v1/events?account_address={account_address}&only_opensea=false&limit=20"

    headers = {"Accept": "application/json"}

    response = requests.get(url, headers=headers)

    context = {
        "assets": response
    }

    return render(request, 'myapp/user_asset_events.html', context)


def address_transactions(request):
    print("This address has many transactions")

