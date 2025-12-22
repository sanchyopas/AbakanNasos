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
from service.models import *
from shop.models import *
from .utils.views import *


from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, get_list_or_404
import openpyxl
import pandas as pd
from django.core.files.images import ImageFile
from django.contrib.auth.decorators import user_passes_test
import uuid
import numpy as np
import math
from pytils.translit import slugify
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
import logging
logger = logging.getLogger(__name__)


general_url_product = "/admin/product/"

path = f"{BASE_DIR}/upload/upload.zip"
path_to_excel = f"{BASE_DIR}/upload/upload.xlsx"
images_folder = f"{BASE_DIR}/upload/image"
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

def parse_excel_column(value):
    """ Превращает ячейку Excel в список значений.
        Пустые ячейки -> [''] (одно пустое значение) """
    if pd.isna(value) or value is None:
        return [''], True  # как список

    # Делаем строки и разделяем
    items = [x.strip() for x in str(value).split(',')]

    # Если после очистки пусто → одно пустое значение
    if not any(items):
        return [''], True

    return items, True

def get_value(values, index, total_count):
    # Если список пустой — вернуть пустую строку
    if not values:
        return ""

    # Если одно значение — использовать его для всех
    if len(values) == 1:
        return values[0]

    # Если значений много — использовать по индексу (если хватает)
    if index < len(values):
        return values[index]

    # Если значений меньше чем моделей — пусто
    return ""


def rename_image(filename):
  original_name = filename

  try:
    # Убираем пробелы по краям
    original_name = original_name.strip()

    # Разделяем имя и расширение
    image_name, ext = os.path.splitext(original_name)
    ext = ext.strip().lower()

    # Генерируем slug
    slug_name = slugify(image_name)

    # Новое имя файла
    new_filename = f"{slug_name}{ext}"

    # Полные пути
    old_path = os.path.join(images_folder, original_name)
    new_path = os.path.join(images_folder, new_filename)

    # Если оригинальный файл существует — переименовываем
    if os.path.exists(old_path):
        os.rename(old_path, new_path)
    else:
      pass
#        print(f"ФАЙЛ НЕ НАЙДЕН: {original_name}")


    return f"goods/{new_filename}"

  except:
    pass

def import_products_from_excel(file_path):
    Product.objects.all().delete()
    Category.objects.all().delete()
    Models.objects.all().delete()

    # Загружаем данные из Excel
    df = pd.read_excel(file_path, engine='openpyxl', skiprows=1)

    for _, row in df.iterrows():
        category = None if pd.isna(row.iloc[0]) else str(row.iloc[0]).strip()
        if not category:
            continue

        category_slug = slugify(category)
        description = "" if pd.isna(row.iloc[2]) else row.iloc[2]
        image = rename_image(row.iloc[3])
        print(image)

        # --- CATEGORY ---
        try:
            category_obj = Category.objects.get(slug=category_slug)
        except ObjectDoesNotExist:
            category_obj = Category.objects.create(
                name=category,
                slug=category_slug,
                image=image,
                status='published'
            )

        # --- PRODUCT ---
        name = row.iloc[1]
        if pd.isna(name) or not str(name).strip():
            continue

        slug = get_unique_slug(Product, slugify(name))
        product_image = rename_image(row.iloc[4])

        try:
            new_product = Product.objects.create(
                name=name,
                slug=slug,
                image=product_image,
                description=description,
                status='published'
            )
        except IntegrityError:
            slug = get_unique_slug(Product, slug)
            new_product = Product.objects.create(
                name=name,
                slug=slug,
                image=product_image,
                description=description,
                status='published'
            )

        new_product.category.add(category_obj)

        # --- MODELS ---
        try:
            models_image, _ = parse_excel_column(row.iloc[5])
            models_list, _ = parse_excel_column(row.iloc[6])
            power_list, _ = parse_excel_column(row.iloc[7])
            el_network_list, _ = parse_excel_column(row.iloc[8])
            nom_capacity_list, _ = parse_excel_column(row.iloc[9])
            max_capacity_list, _ = parse_excel_column(row.iloc[10])
            max_capacity_min_list, _ = parse_excel_column(row.iloc[11])
            now_head_list, _ = parse_excel_column(row.iloc[12])
            max_head_list, _ = parse_excel_column(row.iloc[13])
            suction_depth_list, _ = parse_excel_column(row.iloc[14])
            con_size_list, _ = parse_excel_column(row.iloc[15])

            count = len(models_list)

            for i in range(count):
                model_name = get_value(models_list, i, count)
                if not model_name:
                    continue

                # уникальный slug для каждой модели
                model_slug = get_unique_slug(Models, slugify(model_name))

                # --- ОБРАБОТКА КАРТИНКИ МОДЕЛИ ---
                raw_model_image = get_value(models_image, i, count)
                model_image = rename_image(raw_model_image) if raw_model_image else None

                # создаем модель
                model_obj, created = Models.objects.get_or_create(
                    parent=new_product,
                    slug=model_slug,
                    defaults={
                        'image': model_image,
                        'model': model_name,
                        'power': get_value(power_list, i, count),
                        'el_network': get_value(el_network_list, i, count),
                        'nom_capacity': get_value(nom_capacity_list, i, count),
                        'max_capacity': get_value(max_capacity_list, i, count),
                        'max_capacity_min': get_value(max_capacity_min_list, i, count),
                        'now_head': get_value(now_head_list, i, count),
                        'max_head': get_value(max_head_list, i, count),
                        'suction_depth': get_value(suction_depth_list, i, count),
                        'con_size': get_value(con_size_list, i, count),
                        'status': 'published'
                    }
                )

        except Exception as e:
            print("Ошибка при импорте модели:", e)




# @user_passes_test(lambda u: u.is_superuser)
import urllib.parse

@user_passes_test(lambda u: u.is_superuser)
def admin(request):
  import_products_from_excel(path_to_excel)

  # unzip_archive()
  """Данная предстовление отобразает главную страницу админ панели"""
  return render(request, "page/index.html")

@user_passes_test(lambda u: u.is_superuser)
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

folder = 'upload/'

from PIL import Image

@user_passes_test(lambda u: u.is_superuser)
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

@user_passes_test(lambda u: u.is_superuser)
def upload_succes(request):
  return render(request, "upload/upload-succes.html")

# Новые views

""" Общие настройки сайта """
@user_passes_test(lambda u: u.is_superuser)
def admin_settings(request):
  return generic_singleton_edit(request, GlobalSettingsForm, BaseSettings, "Общие настройки", template_name=None)


""" Социальные сети """
@user_passes_test(lambda u: u.is_superuser)
def socials(request):
    return generic_list(request, Socials, "Соц.сети", "socials_add", "socials_edit", "socials_delete")

@user_passes_test(lambda u: u.is_superuser)
def socials_add(request):
    return generic_add(request, SocialsForm, "socials", "Добавление соц.сети",  template_name=None)

@user_passes_test(lambda u: u.is_superuser)
def socials_edit(request, pk):
  return generic_edit(request, pk, Socials, SocialsForm, "socials", "Редактирование соц.сети",  template_name=None)

@user_passes_test(lambda u: u.is_superuser)
def socials_delete(request, pk):
    return generic_delete(request, Socials, pk)


""" Слайдеры """

@user_passes_test(lambda u: u.is_superuser)
def sliders(request):
    return generic_list(request, SliderHero, "Слайдер", "sliders_add", "sliders_edit", "sliders_delete")

@user_passes_test(lambda u: u.is_superuser)
def sliders_add(request):
    return generic_add(request, SliderHeroForm, "sliders", "Добавление слайда",  template_name=None)

@user_passes_test(lambda u: u.is_superuser)
def sliders_edit(request, pk):
  return generic_edit(  request,  pk, SliderHero,  SliderHeroForm, "sliders", "Редактирование слайда", template_name=None)

@user_passes_test(lambda u: u.is_superuser)
def sliders_delete(request, pk):
    return generic_delete(request, SliderHero, pk)


""" Филиалы """
@user_passes_test(lambda u: u.is_superuser)
def admin_branch(request):
  return generic_list(request, Branch, "Филиалы", "branch_add", "branch_edit", "branch_delete")

@user_passes_test(lambda u: u.is_superuser)
def branch_add(request):
  return generic_add(request, BranchForm, "admin_branch", "Добавление Филиала",  template_name=None)

@user_passes_test(lambda u: u.is_superuser)
def branch_edit(request, pk):
  return generic_edit(  request,  pk, Branch,  BranchForm, "admin_branch", "Редактирование Филиала", template_name=None)

@user_passes_test(lambda u: u.is_superuser)
def branch_delete(request, pk):
  return generic_delete(request, Branch, pk)


""" Блок callback на главной странице """
@user_passes_test(lambda u: u.is_superuser)
def admin_callback_block(request):
  return generic_singleton_edit(request, CallBackBlockForm, CallBackBlock, "Настройки блока", template_name=None)


""" Настройки главной страницы """
@user_passes_test(lambda u: u.is_superuser)
def admin_home_page(request):
  return generic_singleton_edit(request,
  HomeTemplateForm,
  HomeTemplate,
  "Настройки главной страницы",
  template_name="common-template/singleton_page_edit.html"
  )


""" Настройки страницы о нас """
@user_passes_test(lambda u: u.is_superuser)
def admin_about_page(request):
  return generic_singleton_edit(request, AboutPageForm, AboutPage, "Настройки страницы о нас", template_name=None)


""" Настройки страницы о нас """
@user_passes_test(lambda u: u.is_superuser)
def admin_contact_page(request):
  return generic_singleton_edit(request, ContactPageForm, ContactPage, "Настройки страницы контакты", template_name=None)


""" Настройки страницы блога """
@user_passes_test(lambda u: u.is_superuser)
def blog_settings(request, **extra_context):
    try:
      instance = BlogSettings.objects.get()
      items = Post.objects.all()
      category = BlogCategory.objects.all()
    except BlogSettings.DoesNotExist:
      instance = BlogSettings()
      items = Post()
      category = BlogCategory()
      instance.save()
    except Exception as e:
      messages.error(request, f"Ошибка: {e}")
      return redirect(request.META.get('HTTP_REFERER'))

    if request.method == "POST":
      print(request.method)
      form = BlogSettingsForm(request.POST, request.FILES, instance=instance)

      if form.is_valid():
        print('this')
        try:
          saved_instance = form.save()
          messages.success(request, "Успешно сохранено!")
          return redirect(request.META.get('HTTP_REFERER'))
        except Exception as e:
          messages.error(request, f"Ошибка сохранения: {e}")
      else:
        return render(request, "common-template/generic_page_editor.html", {
          "form": form,
          "title": "Настройки блога",
          "settings": instance,
          "items": items,
          "category": category,
          "edit_url": "post_edit",
          "delete_url": "post_delete",
        })

    form = BlogSettingsForm(instance=instance)

    context = {
      "form": form,
      "title": "Настройки блога",
      "settings": instance,
      "items": items,
      "add_url": "post_add",
      "edit_url": "post_edit",
      "delete_url": "post_delete"
    }

    return render(request,"common-template/generic_page_editor.html", context)


""" Категории товаров """
@user_passes_test(lambda u: u.is_superuser)
def admin_category(request):
  return generic_list(request, Category, "Категории", "category_add", "category_edit", "category_delete")

@user_passes_test(lambda u: u.is_superuser)
def category_add(request):
  return generic_add(request, CategoryForm, "admin_category", "Добавление категории",  template_name=None)

@user_passes_test(lambda u: u.is_superuser)
def category_edit(request, pk):
  return generic_edit(  request,  pk, Category,  CategoryForm, "admin_category", "Редактирование категории", template_name=None)

@user_passes_test(lambda u: u.is_superuser)
def category_delete(request, pk):
  return generic_delete(request, Category, pk)


""" Настройки страницы каталога """
@user_passes_test(lambda u: u.is_superuser)
def admin_shop(request):
  return generic_singleton_edit(
  request,
  ShopSettingsForm,
  ShopSettings,
  "Настройки страницы каталога",
  template_name="common-template/singleton_page_edit.html",
  )

""" Товары """
@user_passes_test(lambda u: u.is_superuser)
def admin_product(request):
  return generic_list(request, Product, "Товары", "product_add", "product_edit", "product_delete")

@user_passes_test(lambda u: u.is_superuser)
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

      messages.success(request, "Успешно сохранено !")
      return redirect(request.META.get('HTTP_REFERER'))
    else:
      error_list = []

      for field_name, errors in form.errors.items():
        if field_name == "__all__":
          for error in errors:
            error_list.append(error)
          continue
        field_label = form[field_name].label

        for error in errors:
          error_list.append(f"{field_label}: {error}")
      messages.error(request, " | ".join(error_list))
      return render(request, 'common-template/product-edit-add-page.html', {'form': form_new})

  context = {
    "form": form,
    "title": "Страница редактирования",
    "url": general_url_product,
    "images": images,
  }

  return render(request, "common-template/product-edit-add-page.html", context)

@user_passes_test(lambda u: u.is_superuser)
def product_add(request):
  return generic_add(request, ProductForm, "admin_shop", "Добавление Товара",  template_name="common-template/product-edit-add-page.html")

@user_passes_test(lambda u: u.is_superuser)
def product_delete(request,pk):
  return generic_delete(request, Product, pk)


""" Модели товаров """
@user_passes_test(lambda u: u.is_superuser)
def admin_model(request):
  return generic_list(request, Models, "Модели", "model_add", "model_edit", "model_delete")

@user_passes_test(lambda u: u.is_superuser)
def model_add(request):
  return generic_add(request, ModelsForm, "admin_model", "Добавление модели",  template_name=None)

@user_passes_test(lambda u: u.is_superuser)
def model_edit(request, pk):
  return generic_edit(  request,  pk, Models,  ModelsForm, "admin_model", "Редактирование модели", template_name=None)

@user_passes_test(lambda u: u.is_superuser)
def model_delete(request, pk):
  return generic_delete(request, Models, pk)


""" Наши клиенты блок """
@user_passes_test(lambda u: u.is_superuser)
def admin_clients(request):
  return generic_list(request, Clients, "Наши клиенты", "clients_add", "clients_edit", "clients_delete")

@user_passes_test(lambda u: u.is_superuser)
def clients_add(request):
  return generic_add(request, ClientsForm, "admin_clients", "Добавление блока",  template_name=None)

@user_passes_test(lambda u: u.is_superuser)
def clients_edit(request, pk):
  return generic_edit(  request,  pk, Clients,  ClientsForm, "admin_clients", "Редактирование блока", template_name=None)

@user_passes_test(lambda u: u.is_superuser)
def clients_delete(request, pk):
  return generic_delete(request, Clients, pk)


""" Настройки блога """
@user_passes_test(lambda u: u.is_superuser)
def admin_post(request):
  return generic_list(request, Post, "Статьи", "post_add", "post_edit", "post_delete")

@user_passes_test(lambda u: u.is_superuser)
def post_add(request):
  return generic_add(request, PostForm, "admin_post", "Добавление статьи",  template_name=None)

@user_passes_test(lambda u: u.is_superuser)
def post_edit(request, pk):
  return generic_edit(  request,  pk, Post,  PostForm, "admin_post", "Редактирование статьи", template_name=None)

@user_passes_test(lambda u: u.is_superuser)
def post_delete(request, pk):
  return generic_delete(request, Post, pk)


""" Настройки категорий блога """
@user_passes_test(lambda u: u.is_superuser)
def category_blog(request):
  return generic_list(request, BlogCategory, "Категории статей", "category_blog_add", "category_blog_edit", "category_blog_delete")

@user_passes_test(lambda u: u.is_superuser)
def category_blog_add(request):
  return generic_add(request, BlogCategoryForm, "category_blog", "Добавление категории статей",  template_name=None)

@user_passes_test(lambda u: u.is_superuser)
def category_blog_edit(request, pk):
  return generic_edit(request,  pk, BlogCategory,  BlogCategoryForm, "category_blog", "Редактирование категории статей", template_name=None)

@user_passes_test(lambda u: u.is_superuser)
def category_blog_delete(request, pk):
  return generic_delete(request, BlogCategory, pk)


""" Настройки Галереи """
@user_passes_test(lambda u: u.is_superuser)
def gallery_settings(request):
  return generic_singleton_edit(request, GalleryPageForm, GalleryPage, "Настройки страницы галерея", template_name=None)

@user_passes_test(lambda u: u.is_superuser)
def gallery_add(request):
  return generic_add(request, GalleryItemForm, "gallery_settings", "Добавление фотографии",  template_name=None)

@user_passes_test(lambda u: u.is_superuser)
def gallery_edit(request, pk):
  return generic_edit(request,  pk, GalleryItem,  GalleryItemForm, "gallery_settings", "Редактирование фотографии", template_name=None)

@user_passes_test(lambda u: u.is_superuser)
def gallery_delete(request, pk):
  return generic_delete(request, GalleryItem, pk)


""" Настройки услуг """
@user_passes_test(lambda u: u.is_superuser)
def admin_services(request):
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

@user_passes_test(lambda u: u.is_superuser)
def services_add(request):
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

@user_passes_test(lambda u: u.is_superuser)
def services_edit(request, pk):
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

@user_passes_test(lambda u: u.is_superuser)
def services_delete(request, pk):
  service = Service.objects.get(id=pk)
  service.delete()
  url = reverse("admin_service_page") + "?tab=list"
  return redirect(url)

