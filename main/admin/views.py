import math
import os
import zipfile
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import messages
from admin.forms import *
from home.models import *
from blog.models import BlogSettings, Post, BlogCategory
from main.settings import BASE_DIR
from subdomain.models import Subdomain
from service.models import Service, ServicePage

from shop.models import ColorProduct, Product, Category, ProductImage, Properties, ShopSettings
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, get_list_or_404
import openpyxl
import pandas as pd
from django.core.files.images import ImageFile
from django.contrib.auth.decorators import user_passes_test
import uuid
import numpy as np
import math

general_url_product = "/admin/product/"

path = f"{BASE_DIR}/upload/upload.zip"
path_to_excel = f"{BASE_DIR}/upload/upload.xlsx"
folder = 'upload/'

def unzip_archive():
  with zipfile.ZipFile(path, 'r') as zip_ref:
    zip_ref.extractall()


def get_unique_slug(model, base_slug):
    slug = base_slug
    counter = 1
    while model.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    return slug

def import_products_from_excel(file_path):
    Product.objects.all().delete()
    Properties.objects.all().delete()
    Category.objects.all().delete()

    # Загружаем данные из Excel
    df = pd.read_excel(file_path, engine='openpyxl')

    for _, row in df.iterrows():
      article=row[0]
      name = row[1].strip()
      slug = get_unique_slug(Product, slugify(name))
      category = row[2]
      category_slug = slugify(category)

      try:
        category = Category.objects.get(slug=category_slug)
      except ObjectDoesNotExist:
        if not Category.objects.filter(name=category).exists():
          category = Category.objects.create(
            name=category,
            slug=category_slug
        )
      try:
        manufacturer = row[3]
      except:
        pass

      manufacturer_description = row[4]

      try:
        colors = row[5]
        if isinstance(colors, float) and math.isnan(colors):  # Проверяем, является ли значением NaN
          colors = ""
      except:
        colors = ""

      image = f"goods/{row[6]}"


      try:
          price = row[7]
          if isinstance(price, float) and math.isnan(price):  # Проверяем, является ли значением NaN
            price = 0
      except:
          price = 0

      try:
        installment = row[8]
        if isinstance(installment, float) and math.isnan(installment):  # Проверяем, является ли значением NaN
          installment = ""
      except:
        installment = ""

      try:
          properties = row[10]
      except:
          properties = ""

      sale = 0

      try:
          new_product = Product.objects.create(
              article=article,
              name=name,
              slug=slug,
              category=category,
              manufacturer=manufacturer,
              manufacturer_description=manufacturer_description,
              colors=colors,
              image=image,
              price=price,
              installment=installment,
              sale=sale,
          )
      except IntegrityError:
          print(f"Duplicate slug detected: {slug}, generating a new one.")
          slug = get_unique_slug(Product, slug)
          new_product = Product.objects.create(
              article=article,
              name=name,
              slug=slug,
              category=category,
              manufacturer=manufacturer,
              manufacturer_description=manufacturer_description,
              colors=colors,
              image=image,
              price=price,
              installment=installment,
              sale=sale,
          )

      try:
          properties = properties.split(';')
          for ch in properties:
            try:
              new_properties = Properties.objects.create(
                parent = new_product,
                name = ch.split(":")[0].strip(),
                value = ch.split(":")[1].strip()
              )
            except Exception as e:
                pass
      except:
          pass

# @user_passes_test(lambda u: u.is_superuser)
# def sidebar_show(request): 
   
#     request.session['sidebar'] = 'True'
    
#     return redirect('admin')

# @user_passes_test(lambda u: u.is_superuser)
import urllib.parse

@user_passes_test(lambda u: u.is_superuser)
def admin(request):
  #import_products_from_excel(path_to_excel)

  # unzip_archive()
  """Данная предстовление отобразает главную страницу админ панели"""
  return render(request, "page/index.html")

def admin_settings(request):
  try:
    settings = BaseSettings.objects.get()
  except:
    settings = BaseSettings()
    settings.save()
  
  if request.method == "POST":
    form_new = GlobalSettingsForm(request.POST, request.FILES, instance=settings)
    if form_new.is_valid():
      form_new.save()
      
      # subprocess.call(["touch", RESET_FILE])
      return redirect(request.META.get('HTTP_REFERER'))
    else:
      return render(request, "settings/general_settings.html", {"form": form_new})

  settings = BaseSettings.objects.get()

  form = GlobalSettingsForm(instance=settings)
  context = {
    "form": form,
    "settings":settings
  }  

  return render(request, "settings/general_settings.html", context)

def robots(request):
  try:
    robots = RobotsTxt.objects.get()
  except:
    robots = RobotsTxt()
    robots.save()
  
  if request.method == "POST":
    form_new = RobotsForm(request.POST, request.FILES, instance=robots)
    if form_new.is_valid():
      form_new.save()
      
      return redirect(request.META.get('HTTP_REFERER'))
    else:
      return render(request, "settings/robots.html", {"form": form_new})

  robots = RobotsTxt.objects.get()

  form = RobotsForm(instance=robots)
  
  context = {
    "form": form,
    "robots":robots
  }  

  return render(request, "settings/robots.html", context)

def admin_product(request):
  """
  View, которая возвращаяет и отрисовывает все товары на странице
  и разбивает их на пагинацию
  """
  page = request.GET.get('page', 1)
  products = Product.objects.all()
  paginator = Paginator(products, 20)
  current_page = paginator.page(int(page))

  context = {
    "items": current_page
  }
  return render(request, "shop/product/product.html", context)

def product_edit(request, pk):
  """
    View, которая получает данные из формы редактирования товара
    и изменяет данные внесенные данные товара в базе данных
  """
  product = Product.objects.get(id=pk)
  product_image = ProductImage.objects.filter(parent=product)
  all_chars = Properties.objects.filter(parent=product)
  properties_form = ProductPropertiesForm()

  form = ProductForm(instance=product)

  form_new = ProductForm(request.POST, request.FILES, instance=product)

  if request.method == 'POST':
      if form_new.is_valid():
          form_new.save()
          product = Product.objects.get(id=pk)

          # Добавление новых характеристик
          prop_names = request.POST.getlist('new_name')
          prop_values = request.POST.getlist('new_value')

          for i in range(min(len(prop_names), len(prop_values))):
            Properties.objects.create(
                name=prop_names[i].strip(),
                value=prop_values[i].strip(),
                parent=product
            )

          # Обновление старых характеристик
          old_ids = request.POST.getlist('old_id')
          old_names = request.POST.getlist('old_name')
          old_values = request.POST.getlist('old_value')

          for i in range(min(len(old_ids), len(old_names), len(old_values))):
              prop = Properties.objects.get(id=old_ids[i])
              prop.name = old_names[i]
              prop.value = old_values[i]
              prop.save()


          images = request.FILES.getlist('src')

          for image in images:
              img = ProductImage(parent=product, src=image)
              img.save()

          return redirect(request.META.get('HTTP_REFERER'))
      else:
          return render(request, 'common-template/template-edit-add-page.html', {'form': form_new})
  context = {
    "form":form,
    "all_chars": all_chars,
    "title": "Страница редактирования",
    "url": general_url_product,
    "properties_form":properties_form,
    "product_image": product_image,
  }
  return render(request, "common-template/template-edit-add-page.html", context)

def product_add(request):
  form = ProductForm()

  if request.method == "POST":
    form_new = ProductForm(request.POST, request.FILES)
    if form_new.is_valid():
      form_new.save()
      return redirect('admin_product')
    else:
      return render(request, "common-template/template-edit-add-page.html", {"form": form_new})

  context = {
   "title": "Страница добавление",
   "url": general_url_product,
   "form": form
  }

  return render(request, 'common-template/template-edit-add-page.html', context)

def product_delete(request,pk):
  product = Product.objects.get(id=pk)
  product.delete()

  return redirect('admin_product')

def delete_properties(request,pk):
  propertie = Properties.objects.get(id=pk)
  propertie.delete()

  return redirect(request.META.get('HTTP_REFERER'))

def admin_home_page(request):
  try:
    settings = HomeTemplate.objects.get()
  except:
    settings = HomeTemplate()
    settings.save()
  
  if request.method == "POST":
    form_new = HomeTemplateForm(request.POST, request.FILES, instance=settings)
    if form_new.is_valid():
      form_new.save()
      
      # subprocess.call(["touch", RESET_FILE])
      return redirect(request.META.get('HTTP_REFERER'))
    else:
      return render(request, "home-page/home-page.html", {"form": form_new})

  settings = HomeTemplate.objects.get()

  form = HomeTemplateForm(instance=settings)
  context = {
    "form": form,
    "settings":settings
  }  

  return render(request, "home-page/home-page.html", context)

def admin_prod_page(request):
  try:
    settings = Production.objects.get()
  except:
    settings = Production()
    settings.save()

  if request.method == "POST":
    form_new = ProductionForm(request.POST, request.FILES, instance=settings)
    if form_new.is_valid():
      form_new.save()

      # subprocess.call(["touch", RESET_FILE])
      return redirect(request.META.get('HTTP_REFERER'))
    else:
      return render(request, "page/production.html", {"form": form_new})

  settings = Production.objects.get()

  form = ProductionForm(instance=settings)
  context = {
    "form": form,
    "settings":settings
  }

  return render(request, "page/production.html", context)

def admin_contact(request):
  try:
    settings = ContactTemplate.objects.get()
  except:
    settings = ContactTemplate()
    settings.save()

  if request.method == "POST":
    form_new = ContactTemplateForm(request.POST, request.FILES, instance=settings)
    if form_new.is_valid():
      form_new.save()

      # subprocess.call(["touch", RESET_FILE])
      return redirect(request.META.get('HTTP_REFERER'))
    else:
      return render(request, "page/contact.html", {"form": form_new})

  settings = ContactTemplate.objects.get()

  form = ContactTemplateForm(instance=settings)
  context = {
    "form": form,
    "settings": settings
  }

  return render(request, "page/contact.html", context)

def admin_about_page(request):
  try:
    settings = About.objects.get()
  except:
    settings = About()
    settings.save()

  if request.method == "POST":
    form_new = AboutTemplateForm(request.POST, request.FILES, instance=settings)
    if form_new.is_valid():
      form_new.save()

      # subprocess.call(["touch", RESET_FILE])
      return redirect(request.META.get('HTTP_REFERER'))
    else:
      return render(request, "template-page/about_page.html", {"form": form_new})

  settings = About.objects.get()

  form = AboutTemplateForm(instance=settings)
  context = {
    "form": form,
    "settings":settings
  }

  return render(request, "template-page/about_page.html", context)

def admin_delivery_page(request):
  try:
    settings = Delivery.objects.get()
  except:
    settings = Delivery()
    settings.save()

  if request.method == "POST":
    form_new = DeliveryForm(request.POST, request.FILES, instance=settings)
    if form_new.is_valid():
      form_new.save()

      # subprocess.call(["touch", RESET_FILE])
      return redirect(request.META.get('HTTP_REFERER'))
    else:
      return render(request, "template-page/delivery_page.html", {"form": form_new})

  settings = Delivery.objects.get()

  form = DeliveryForm(instance=settings)
  context = {
    "form": form,
    "settings":settings
  }

  return render(request, "template-page/delivery_page.html", context)

@user_passes_test(lambda u: u.is_superuser)
def admin_shop(request):
  try:
    shop_setup = ShopSettings.objects.get()
    form = ShopSettingsForm(instance=shop_setup)
  except:
    form = ShopSettingsForm()
    
  if request.method == "POST":
    try:
      shop_setup = ShopSettings.objects.get()
    except ShopSettings.DoesNotExist:
      shop_setup = None
    form_new = ShopSettingsForm(request.POST, request.FILES, instance=shop_setup)
    
    if form_new.is_valid:
      form_new.save()
      
      return redirect('admin_shop')
    else:
      return render(request, "shop/settings.html", {"form": form})
  
  context = {
    "form": form,
  }  
  return render(request, "shop/settings.html", context)

def blog_settings(request):
  try:
    setup = BlogSettings.objects.get()
    form = BlogSettingsForm(instance=setup)
  except:
    form = BlogSettingsForm()
    
  if request.method == "POST":
    try:
      setup = BlogSettings.objects.get()
    except BlogSettings.DoesNotExist:
      setup = None
    form_new = BlogSettingsForm(request.POST, request.FILES, instance=setup)
    
    if form_new.is_valid:
      form_new.save()
      
      return redirect('.')
    else:
      return render(request, "blog/settings.html", {"form": form})
  
  context = {
    "form": form,
  }  
  return render(request, "blog/settings.html", context)

def gallery_settings(request):
  try:
    home_page = GalleryCategory.objects.get()
  except:
    home_page = GalleryCategory()
    home_page.save()

  if request.method == "POST":
    form_new = GalleryCategoryForm(request.POST, request.FILES, instance=home_page)
    if form_new.is_valid():
      form_new.save()

      # subprocess.call(["touch", RESET_FILE])
      return redirect(".")
    else:
      return render(request, "gallery/gallery_settings.html", {"form": form_new})

  home_page = GalleryCategory.objects.get()
  works = Gallery.objects.all()
  work_list = Works.objects.all()
  form = GalleryCategoryForm(instance=home_page)
  context = {
    "form": form,
    "home_page":home_page,
    "items":works,
    "works": work_list
  }

  return render(request, "gallery/gallery_settings.html", context)



def admin_attribute(request):
  chars = ProductSpecification.objects.all()
  
  context = {
    "title": "Характеристики товара",
    "chars": chars,
  }
  
  return render(request, "shop/char/char.html", context)

folder = 'upload/'

from PIL import Image

def upload_goods(request):
    form = UploadFileForm()
    if request.method == 'POST':
      form = UploadFileForm(request.POST, request.FILES)
      if form.is_valid():
          file = request.FILES['file']
          
          destination = open(os.path.join('upload/', file.name), 'wb+')
          for chunk in file.chunks():
              destination.write(chunk)
          destination.close()
              
          # Распаковка архива
          with zipfile.ZipFile('upload/upload.zip', 'r') as zip_ref:
              zip_ref.extractall('media/')
              
          # Удаление загруженного архива
          os.remove('upload/upload.zip')
          
          # Сжатие фотографий
          for filename in os.listdir('media/upload'):
            
            if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.JPG') or filename.endswith('.JPEG') or filename.endswith('.jpeg'):
              with Image.open(os.path.join('media/upload', filename)) as img:
                temp = filename.replace('.jpeg', '')
                temp_one = temp.replace('№', '')
                temp_b = temp_one.replace('В', 'B')
                temp_e = temp_one.replace('Э', 'E')
                img.save(os.path.join('media/goods', temp_e), quality=60)  # quality=60 для JPEG файла
                
          # Очистка временной папки
          os.system('rm -rf media/upload')
          return redirect('upload-succes')
      else:
        form = UploadFileForm()
    return render(request, 'upload/upload.html', {'form': form})

def upload_succes(request):
  return render(request, "upload/upload-succes.html")

from pytils.translit import slugify
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

def admin_category(request):
  categorys = Category.objects.filter(parent__isnull=True)
  
  context ={
    "items": categorys,
  }
  return render(request, "shop/category/category.html", context)

def category_add(request):
  form = CategoryForm()
  if request.method == "POST":
    form_new = CategoryForm(request.POST, request.FILES)
    if form_new.is_valid():
      form_new.save()
      return redirect("admin_category")
    else:
      return render(request, "shop/category/category_add.html", {"form": form_new})
    
  context = {
    "form": form
  }
  return render(request, "shop/category/category_add.html", context)

def category_edit(request, pk):
  category = Category.objects.get(id=pk)

  form = CategoryForm(request.POST, request.FILES, instance=category)
  
  if request.method == "POST":
    
    if form.is_valid():
      form.save()
      return redirect("admin_category")
    else:
      return render(request, "shop/category/category_edit.html", {"form": form, 'image_path': image_path})
  
  context = {
    "form": CategoryForm(instance=category),
    "categorys": category
  }

  return render(request, "shop/category/category_edit.html", context)

def category_delete(request, pk):
  category = Category.objects.get(id=pk)
  category.delete()
  
  return redirect('admin_category')

def admin_home(request):
  try:
    home_page = HomeTemplate.objects.get()
  except:
    home_page = HomeTemplate()
    home_page.save()
    
  if request.method == "POST":
    form_new = HomeTemplateForm(request.POST, request.FILES, instance=home_page)
    if form_new.is_valid():
      form_new.save()
      
      # subprocess.call(["touch", RESET_FILE])
      return redirect("admin")
    else:
      return render(request, "static/home_page.html", {"form": form_new})
  
  home_page = HomeTemplate.objects.get()
  
  form = HomeTemplateForm(instance=home_page)
  context = {
    "form": form,
    "home_page":home_page
  }  
  
  return render(request, "static/home_page.html", context)

def admin_service_page(request):
  try:
     serv_page = ServicePage.objects.get()
  except:
     serv_page = ServicePage()
     serv_page.save()

  try:
    items = Service.objects.all()
  except:
    items = Service()

  if request.method == "POST":
     form_new = ServicePageForm(request.POST, request.FILES, instance=serv_page)
     if form_new.is_valid():
       form_new.save()

       return redirect(request.META.get('HTTP_REFERER'))
     else:
       return render(request, "serv/serv_settings.html", {"form": form_new})

  serv_page = ServicePage.objects.get()

  form = ServicePageForm(instance=serv_page)
  context = {
     "form": form,
     "serv_page":serv_page,
     "items": items
  }
  
  return render(request, "serv/serv_settings.html", context)

def admin_stock(request):
  stocks = Stock.objects.all()

  context = {
    "stocks": stocks
  }

  return render(request, "stock/stock.html", context)

def stock_add(request):
  form = StockForm()
  
  if request.method == "POST":
    form_new = StockForm(request.POST, request.FILES)
    if form_new.is_valid():
      form_new.save()
      return redirect("admin_stock")
    else: 
      return render(request, "stock/stock_add.html", {"form": form_new})
  
  context = {
    "form": form
  }
  
  return render(request, "stock/stock_add.html", context)

def stock_edit(request, pk):
  stock = Stock.objects.get(id=pk)
  form = StockForm(instance=stock)
  if request.method == "POST":
    form_new = StockForm(request.POST, request.FILES, instance=stock)
    if form_new.is_valid():
      form_new.save()
      return redirect("admin_stock")
    else:
      return render(request, "stock/stock_edit.html", {"form": form_new})
  
  context = {
    "form": form
  }
  
  return render(request, "stock/stock_edit.html", context)

def stock_delete(request, pk):
  stock = Stock.objects.get(id=pk)
  stock.delete()
  return redirect("admin_stock")

def service_add(request):
  form = ServiceForm()
  
  if request.method == "POST":
    form_new = ServiceForm(request.POST, request.FILES)
    if form_new.is_valid():
      form_new.save()
      url = reverse("admin_service_page") + "?tab=list"
      return redirect(url)
    else: 
      return render(request, "serv/serv_add.html", {"form": form_new})
  
  context = {
    "form": form
  }
  
  return render(request, "serv/serv_add.html", context)

def service_edit(request, pk):
  services = Service.objects.get(id=pk)
  form = ServiceForm(instance=services)
  if request.method == "POST":
    form_new = ServiceForm(request.POST, request.FILES, instance=services)
    if form_new.is_valid():
      form_new.save()
      url = reverse("admin_service_page") + "?tab=list"
      return redirect(url)
    else:
      return render(request, "serv/stock_edit.html", {"form": form_new})
  
  context = {
    "form": form
  }
  
  return render(request, "serv/serv_edit.html", context)

def service_delete(request, pk):
  service = Service.objects.get(id=pk)
  service.delete()
  url = reverse("admin_service_page") + "?tab=list"
  return redirect(url)

def admin_color(request):
  items = ColorProduct.objects.all()
  
  context = {
    "items": items,  
  }
  
  return render(request, "shop/color/color.html", context)


def admin_color_add(request):
  form = ColorProductForm()
  
  if request.method == "POST":
    form_new = ColorProductForm(request.POST, request.FILES)
    if form_new.is_valid():
      form_new.save()
      return redirect('admin_color')
    else:
      return render(request, "shop/color/color_add.html", { "form": form_new })
    
  context = {
    "form": form, 
  }  
    
  return render(request, "shop/color/color_add.html", context)

def admin_color_edit(request, pk):
  item = ColorProduct.objects.get(id=pk)
  
  if request.method == "POST":
    form_new = ColorProductForm(request.POST, request.FILES, instance=item)
    
    if form_new.is_valid():
      form_new.save()
      return redirect('admin_color')
    else:
      return render(request, "shop/color/color_edit.html", { "form": form_new })
  
  form = ColorProductForm(instance=item)
  context = {
    "form": form,
  }  
    
  return render(request, "shop/color/color_edit.html", context)

def admin_color_delete(request, pk):
  subdomain = Subdomain.objects.get(id=pk)
  subdomain.delete()
  return redirect(request.META.get('HTTP_REFERER'))

def admin_gallery(request):
  items = Gallery.objects.all()
  
  context = {
    "items": items,  
  }
  
  return render(request, "gallery/gallery.html", context)


def admin_gallery_add(request):
  form = GalleryForm()
  
  if request.method == "POST":
    form_new = GalleryForm(request.POST, request.FILES)
    if form_new.is_valid():
      form_new.save()
      url = reverse("gallery_settings") + "?tab=list"
      return redirect(url)
    else:
      return render(request, "gallery/gallery_add.html", { "form": form_new })
    
  context = {
    "form": form, 
  }  
    
  return render(request, "gallery/gallery_add.html", context)

def admin_gallery_edit(request, pk):
  item = Gallery.objects.get(id=pk)
  
  if request.method == "POST":
    form_new = GalleryForm(request.POST, request.FILES, instance=item)
    
    if form_new.is_valid():
      form_new.save()
      url = reverse("gallery_settings") + "?tab=list"
      return redirect(url)
    else:
      return render(request, "gallery/gallery_edit.html", { "form": form_new })
  
  form = GalleryForm(instance=item)
  context = {
    "form": form,
  }  
    
  return render(request, "gallery/gallery_edit.html", context)

def admin_gallery_delete(request, pk):
  pass


def admin_work_add(request):
  form = WorksForm()

  if request.method == "POST":
    form_new = WorksForm(request.POST, request.FILES)
    if form_new.is_valid():
      form_new.save()
      url = reverse("gallery_settings") + "?tab=works"
      return redirect(url)
    else:
      return render(request, "works/works_add.html", { "form": form_new })

  context = {
    "form": form,
  }

  return render(request, "works/works_add.html", context)

def admin_work_edit(request, pk):
  item = Works.objects.get(id=pk)

  if request.method == "POST":
    form_new = WorksForm(request.POST, request.FILES, instance=item)

    if form_new.is_valid():
      form_new.save()
      url = reverse("gallery_settings") + "?tab=works"
      return redirect(url)
    else:
      return render(request, "works/works_edit.html", { "form": form_new })

  form = WorksForm(instance=item)
  context = {
    "form": form,
  }

  return render(request, "works/works_edit.html", context)

def admin_work_delete(request, pk):
  pass

def admin_color_delete(request, pk):
  subdomain = Subdomain.objects.get(id=pk)
  subdomain.delete()
  return redirect(request.META.get('HTTP_REFERER'))


def admin_gallery_category(request):
  items = GalleryCategory.objects.all()
  
  context = {
    "items": items,
  }
  
  return render(request, "gallery/gallery_category.html", context)


def gallery_category_add(request):
  form = GalleryCategoryForm()
  
  if request.method == "POST":
    form_new = GalleryCategoryForm(request.POST, request.FILES)
    if form_new.is_valid():
      form_new.save()
      return redirect('admin_gallery_category')
    else:
      return render(request, "gallery/gallery_category_add.html", { "form": form_new })
    
  context = {
    "form": form, 
  }  
    
  return render(request, "gallery/gallery_category_add.html", context)

def gallery_category_edit(request, pk):
  item = GalleryCategory.objects.get(id=pk)
  
  if request.method == "POST":
    form_new = GalleryCategoryForm(request.POST, request.FILES, instance=item)
    
    if form_new.is_valid():
      form_new.save()
      return redirect('admin_gallery')
    else:
      return render(request, "gallery/gallery_category_edit.html", { "form": form_new })
  
  form = GalleryCategoryForm(instance=item)
  context = {
    "form": form,
  }  
    
  return render(request, "gallery/gallery_category_edit.html", context)

def gallery_category_delete(request):
  pass



def article(request):
  items = Post.objects.all()
  
  context ={
    "items": items,
  }
  return render(request, "blog/blog_post/blog_post.html", context)

def article_add(request):
  form = PostForm()
  if request.method == "POST":
    form_new = PostForm(request.POST, request.FILES)
    if form_new.is_valid():
      form_new.save()
      return redirect("article")
    else:
      return render(request, "blog/blog_post/post_add.html", {"form": form_new})
    
  context = {
    "form": form
  }
  
  return render(request, "blog/blog_post/post_add.html", context)

def article_edit(request, pk):
  item = Post.objects.get(id=pk)
  form = PostForm(request.POST, request.FILES, instance=item)
  
  if request.method == "POST":
    
    if form.is_valid():
      form.save()
      return redirect("article")
    else:
      return render(request, "blog/blog_post/post_edit.html", {"form": form, 'image_path': image_path})
  
  context = {
    "form": PostForm(instance=item),
    "item": item
  }

  return render(request, "blog/blog_post/post_edit.html", context)

def article_delete(request, pk):
  category = Post.objects.get(id=pk)
  category.delete()
  
  return redirect(request.META.get("HTTP_REFERER"))

def category_blog_settings(request):
    return render(request, "blog/blog_category/blog_category.html", context)

def category_blog(request):
  items = BlogCategory.objects.all()

  context ={
    "items": items,
  }
  return render(request, "blog/blog_category/blog_category.html", context)

def category_blog_add(request):
  form = BlogCategoryForm()
  if request.method == "POST":
    form_new = BlogCategoryForm(request.POST, request.FILES)
    if form_new.is_valid():
      form_new.save()
      return redirect("category_blog")
    else:
      return render(request, "blog/blog_category/blog_category_add.html", {"form": form_new})

  context = {
    "form": form
  }

  return render(request, "blog/blog_category/blog_category_add.html", context)

def category_blog_edit(request, pk):
  item = BlogCategory.objects.get(id=pk)
  form = BlogCategoryForm(request.POST, request.FILES, instance=item)

  if request.method == "POST":

    if form.is_valid():
      form.save()
      return redirect(request.META.get('HTTP_REFERER'))
    else:
      return render(request, "blog/blog_category/blog_category_edit.html", {"form": form, 'image_path': image_path})

  context = {
    "form": BlogCategoryForm(instance=item),
    "item": item
  }

  return render(request, "blog/blog_category/blog_category_edit.html", context)

def category_blog_remove(request, pk):
  category = BlogCategory.objects.get(id=pk)
  category.delete()

  return redirect(request.META.get('HTTP_REFERER'))

# Новые views

def socials(request):
    items = Socials.objects.all()

    context = {
        "items": items,
        "title": "Социальные сети",
        "add_url": "socials_add"
    }

    return render(request, "common-template/list-items.html", context)

def list_items(request, model, title, add_url):
    items = model.objects.all()

    context = {
        "items": items,
        "title": title,
        "add_url": add_url
    }

    return render(request, "common-template/list-items.html", context)

def socials_add(request):
    form = SocialsForm()
    if request.method == "POST":
        form_new = SocialsForm(request.POST, request.FILES)
        if form_new.is_valid():
          form_new.save()
          return redirect("socials")
        else:
          return render(request, "common-template/template-edit-add-page.html", {"form": form_new})

    context = {
        "form": form,
        "title": "Добавление соц.сетей"
    }

    return render(request, "common-template/template-edit-add-page.html", context)

def socials_edit(request, pk):
  item = Socials.objects.get(id=pk)
  form = SocialsForm(request.POST, request.FILES, instance=item)

  if request.method == "POST":

    if form.is_valid():
        form.save()
        messages.success(request, 'Успешное сохранение!')
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return render(request, "common-template/template-edit-add-page.html", {"form": form, 'image_path': image_path})

  context = {
    "form": SocialsForm(instance=item),
    "item": item
  }

  return render(request, "common-template/template-edit-add-page.html", context)
