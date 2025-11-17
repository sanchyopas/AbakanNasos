from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse
from django.db.models import Q
import itertools
from django.db.models import Count
from .models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json



def category(request):
  try:
    shop_setup = ShopSettings.objects.get()
  except: 
    shop_setup = ShopSettings()

  category = Category.objects.filter(parent=None)

  context = {
    "category":category,
    "shop_setup": shop_setup,
  }

  return render(request, "pages/catalog/category.html", context)
import urllib.parse

def category_detail(request, slug):
  page = request.GET.get("page", 1)
  category = Category.objects.get(slug=slug)
  subcategories = category.children.all()


  context = {
    "category": category,
    "subcategories": subcategories
  }

  return render(request, "pages/catalog/category-details.html", context)

def product(request, slug):
  product = Product.objects.get(slug=slug)
  properties = Properties.objects.filter(parent=product)
  products = Product.objects.filter(status=True).exclude(id=product.id)[:4]
   
  context = {
    "product": product,
    "products": products,
    "properties": properties,
  }

  return render(request, "pages/catalog/product.html", context)

@csrf_exempt
def catalog_search(request):

    if request.method == "POST":
        try:
            result = request.body.decode("utf-8")
            value = json.loads(result).get('value')
            try:
                products = Product.objects.filter(name__icontains=value)
                data = []
                for product in products:

                    try:
                        image  = product.image.url
                    except:
                        image = "/core/theme/mb/images/no-image.png"

                    data.append({
                      'name': product.name,
                      'price': product.price,
                      'url': product.get_absolute_url(),
                      'image': image,
                    })
            except Exception as e:
                print(e)
            return JsonResponse({"value": data})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Invalid JSON'}, status=400)
