import math
import os
import zipfile
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from admin.forms import *
from home.models import *
from blog.models import *
from main.settings import BASE_DIR
from subdomain.models import *
from service.models import *


from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, get_list_or_404
import openpyxl
import pandas as pd
from django.core.files.images import ImageFile
from django.contrib.auth.decorators import user_passes_test
import uuid
import numpy as np
import math

# Проверенные импорты
from shop.models import *
from .utils.views import generic_add, generic_edit, generic_list, generic_delete, generic_singleton_edit

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

def delete_properties(request,pk):
  propertie = Properties.objects.get(id=pk)
  propertie.delete()

  return redirect(request.META.get('HTTP_REFERER'))

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
""" Социальные сети """
def socials(request):
    return generic_list(request, Socials, "Соц.сети", "socials_add", "socials_edit", "socials_delete")

def socials_add(request):
    return generic_add(request,SocialsForm, "socials", "Добавление соц.сети",  template_name=None)

def socials_edit(request, pk):
  return generic_edit(request, pk, Socials, SocialsForm, "socials", "Редактирование соц.сети",  template_name=None)

def socials_delete(request, pk):
    return generic_delete(request, Socials, pk)


""" Слайдеры """

def sliders(request):
    return generic_list(request, SliderHero, "Слайдер", "sliders_add", "sliders_edit", "sliders_delete")

def sliders_add(request):
    return generic_add(request, SliderHeroForm, "slider", "Добавление слайда",  template_name=None)

def sliders_edit(request, pk):
  return generic_edit(  request,  pk, SliderHero,  SliderHeroForm, "slider", "Редактирование слайда", template_name=None)

def sliders_delete(request, pk):
    return generic_delete(request, SliderHero, pk)


""" Филиалы """
def admin_branch(request):
  return generic_list(request, Branch, "Филиалы", "branch_add", "branch_edit", "branch_delete")

def branch_add(request):
  return generic_add(request, BranchForm, "admin_branch", "Добавление Филиала",  template_name=None)

def branch_edit(request, pk):
  return generic_edit(  request,  pk, Branch,  BranchForm, "admin_branch", "Редактирование Филиала", template_name=None)

def branch_delete(request, pk):
  return generic_delete(request, Branch, pk)


""" Блок callback на главной странице """
def admin_callback_block(request):
  return generic_singleton_edit(request, CallBackBlockForm, CallBackBlock, "Настройки блока", template_name=None)


""" Настройки главной страницы """
def admin_home_page(request):
  return generic_singleton_edit(request, HomeTemplateForm, HomeTemplate, "Настройки главной страницы", template_name=None)


""" Настройки страницы каталога """
@user_passes_test(lambda u: u.is_superuser)
def admin_shop(request):
  return generic_singleton_edit(request, ShopSettingsForm, ShopSettings, "Настройки страницы каталога", template_name=None)


""" Категории товаров """
def admin_category(request):
  return generic_list(request, Category, "Категории", "category_add", "category_edit", "category_delete")

def category_add(request):
  return generic_add(request, CategoryForm, "admin_category", "Добавление категории",  template_name=None)

def category_edit(request, pk):
  return generic_edit(  request,  pk, Category,  CategoryForm, "admin_category", "Редактирование категории", template_name=None)

def category_delete(request, pk):
  return generic_delete(request, Category, pk)

""" Товары """
def admin_product(request):
  return generic_list(request, Product, "Товары", "product_add", "product_edit", "product_delete")

def product_edit(request, pk):
  """
    View, которая получает данные из формы редактирования товара
    и изменяет данные внесенные данные товара в базе данных
  """
  product = Product.objects.get(id=pk)
  images = ProductImage.objects.filter(parent_id=pk)
  models = Models.objects.filter(parent_id=pk)
  form = ProductForm(instance=product)
  form_new = ProductForm(request.POST, request.FILES, instance=product)

  if request.method == 'POST':
      if form_new.is_valid():
          form_new.save()
          product = Product.objects.get(id=pk)
          images = request.FILES.getlist('src')

          for image in images:
              img = ProductImage(parent=product, src=image)
              img.save()

          return redirect(request.META.get('HTTP_REFERER'))
      else:
          return render(request, 'common-template/template-edit-add-page.html', {'form': form_new})

  context = {
    "form": form,
    "title": "Страница редактирования",
    "url": general_url_product,
    "images": images,
  }

  if models:
    context["models"] = models

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
    "models": models,
    "title": "Страница добавление",
    "url": general_url_product,
    "form": form
  }

  return render(request, 'common-template/template-edit-add-page.html', context)

def product_delete(request,pk):
  return generic_delete(request, Product, pk)


""" Модели товаров """
def admin_model(request):
  return generic_list(request, Models, "Модели", "model_add", "model_edit", "model_delete")

def model_add(request):
  return generic_add(request, ModelsForm, "admin_model", "Добавление модели",  template_name=None)

def model_edit(request, pk):
  return generic_edit(  request,  pk, Models,  ModelsForm, "admin_model", "Редактирование модели", template_name=None)

def model_delete(request, pk):
  return generic_delete(request, Models, pk)

