from decimal import Decimal
from django.shortcuts import render
import requests
from .models import AlfaBank
from order.models import Order
from shop.models import Product

try:
    login = "r-florens38-api"
    password = "r-florens38*?1"
    token = AlfaBank.objects.get().token
except:
    login = ""
    password = ""
    token = ""

gateway_url = ""

[{'positionId': 1, 'name': 'Букет из кустовых роз и хризантем', 'quantity': {'value': 4500, 'measure': 'шт'}, 'itemAmount': '450000', 'itemCode': 4651, 'itemPrice': '450000'}, 
 {'positionId': 2, 'name': 'Букет с герберами', 'quantity': {'value': 3600, 'measure': 'шт'}, 'itemAmount': '720000', 'itemCode': 4650, 'itemPrice': '360000'}, {'positionId': 3, 'name': 'Композиция в конверте', 'quantity': {'value': 1700, 'measure': 'шт'}, 'itemAmount': '170000', 'itemCode': 4663, 'itemPrice': '170000'}]

def create_payment(order, cart, request):
    returnUrl = "https://" + request.META["HTTP_HOST"] + "/orders/order-succes/"
    failUrl = "https://" + request.META["HTTP_HOST"] + "/orders/order-error/"

    def dec_to_cop(price):
        res = str(round(price, 2))
        res_filter = res.replace(",", "").replace(".", "")
        return res_filter

    items = []
    count = 1
    for item in cart:
        product = Product.objects.get(id=item.product.id)
        i = {
            "positionId": count,
            "name": product.name,
            "quantity": {"value": int(item.quantity), "measure": "шт"},
            "itemAmount": dec_to_cop(Decimal(item.product.sell_price()) * item.quantity),
            "itemCode": product.id,
            "itemPrice": dec_to_cop(Decimal(item.product.sell_price())),
        }
        count += 1
        items.append(i)
    
    sum = 0
    for item in items:
        sum += int(item["itemAmount"])
        
    print(round(sum, 2))
        
    post_data = {
        "userName": login,
        "password": password,
        "orderNumber": order.id,
        "amount": sum,
        "returnUrl": returnUrl,
        "failUrl": failUrl,
        "cartItems": items,
    }
    try:
        r = requests.post("https://alfa.rbsuat.com/payment/rest/register.do", post_data)
    except Exception as e:
        print(e)

    try:
        confirmation_url = r.json()["formUrl"]
        pay_id = r.json()["orderId"]
    except:
        error = r.json()["errorCode"]
        confirmation_url = "/pay-error/" + error + "/"
        pay_id = "0"

    data = {"id": pay_id, "confirmation_url": confirmation_url}
    sum = 0
    return data


def get_status(pay_id):
    order = Order.objects.get(payment_id=pay_id)

    post_data = {
        "userName": login,
        "password": password,
        "orderId": pay_id,
        "orderNumber": order.id,
    }

    r = requests.post(
        "https://web.rbsuat.com/ab/rest/getOrderStatusExtended.do", post_data
    )
    print(r.json())

    status = r.json()["errorCode"]

    data = {"status": status, "order": order}

    return data
