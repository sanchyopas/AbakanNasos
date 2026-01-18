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

  category = Category.objects.filter(parent=None, status='published')

  context = {
    "category":category,
    "settings": settings,
  }

  return render(request, "pages/catalog/category.html", context)
import urllib.parse

def category_detail(request, slug):
  page = request.GET.get("page", 1)
  category = category = get_object_or_404(Category, slug=slug)
  products = Product.objects.filter(status='published', category=category).order_by('order_by')

  if category.children:
    subcategories = Category.objects.filter(parent_id=category)

  context = {
    "subcategories": subcategories,
    "category": category,
    "products": products
  }

  return render(request, "pages/catalog/category-details.html", context)


def product(request, parent, slug):
    product = Product.objects.get(slug=slug)
    category = Category.objects.get(slug=parent)
    images = ProductImage.objects.filter(parent=product)

    # модели текущего продукта
    models_qs = Models.objects.filter(parent=product)

    if not models_qs.exists():
        return render(request, "pages/catalog/product.html", {
            "category": category,
            "product": product,
            "images": images,
            "models": [],
            "columns": [],
            "models_list": [],
        })

    # нужные поля
    FIELDS_TO_SHOW = [
        "model",
        "power",
        "el_network",
        "nom_capacity",
        "max_capacity",
        "max_capacity_min",
        "now_head",
        "max_head",
        "suction_depth",
        "con_size",
    ]

    columns = []
    rows = []

    for field_name in FIELDS_TO_SHOW:
        field = Models._meta.get_field(field_name)
        verbose = field.verbose_name

        has_value = models_qs.exclude(**{field_name: None}).exclude(**{field_name: ""}).exists()

        if has_value:
            columns.append({
                "name": field_name,
                "verbose": verbose,
            })

    context = {
        "category": category,
        "product": product,
        "images": images,
        "models": models_qs,
        "columns": columns,
        "models_list": models_qs,
    }

    return render(request, "pages/catalog/product.html", context)


def model_detail(request, parent, product, model):
  model_obj = get_object_or_404(Models, slug=model)
  product = Product.objects.get(slug=product)
  category = Category.objects.get(slug=parent)

  context = {
    "category": category,
    "product": product,
    "model": model_obj
  }

  return render(request, "pages/catalog/model.html", context)


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
