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
    settings = ShopSettings.objects.get()
  except: 
    settings = ShopSettings()

  category = Category.objects.filter(parent=None)

  context = {
    "category":category,
    "settings": settings,
  }

  return render(request, "pages/catalog/category.html", context)
import urllib.parse

def category_detail(request, category_path):
  page = request.GET.get("page", 1)
  category = Category.objects.get(slug=category_path)
  products = Product.objects.filter(category=category)

  context = {
    "category": category,
    "products": products
  }

  return render(request, "pages/catalog/category-details.html", context)

def product(request, category_path, product_slug):
  product = Product.objects.get(slug=product_slug)
  category = Category.objects.get(slug=category_path)
  images = ProductImage.objects.filter(parent=product)

  print(category)

  context = {
    "category": category,
    "product": product,
    "images": images
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
