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
import urllib.parse


def category(request):
  try:
    settings = ShopSettings.objects.get()
  except: 
    settings = ShopSettings()

  category = Category.objects.filter(parent=None, status='published').order_by('order_by')

  context = {
    "category":category,
    "settings": settings,
  }

  return render(request, "pages/catalog/category.html", context)


def category_detail(request, slug):
  page = request.GET.get("page", 1)
  category = get_object_or_404(Category, slug=slug)
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
    models = Models.objects.filter(parent=product)

#     chars = ModelCharacteristic.objects.get(model=models_qs)

#     print(chars)

    context = {
        "category": category,
        "product": product,
        "images": images,
        "models": models,
    }

    return render(request, "pages/catalog/product.html", context)


def model_detail(request, parent, product, model):
  model = get_object_or_404(Models, slug=model)
  product = Product.objects.get(slug=product)
  category = Category.objects.get(slug=parent)

  context = {
    "category": category,
    "product": product,
    "model": model
  }

  return render(request, "pages/catalog/model.html", context)


def catalog_search(request):
    query = request.GET.get("search", "").strip()

    products = Product.objects.none()
    models = Models.objects.none()
    categories = Category.objects.none()

    if query:
        # Категории
        categories = Category.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query),
            status="published"
        ).distinct()

        # Товары
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query),
            status="published"
        ).prefetch_related("category").distinct()

        # Модели
        models = Models.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query),
            status="published"
        ).select_related("parent").distinct()

    context = {
        "query": query,
        "products": products,
        "models": models,
        "categories": categories,
    }

    return render(request, "pages/catalog/search.html", context)
