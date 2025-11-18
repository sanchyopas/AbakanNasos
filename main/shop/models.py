from django.db import models
from django.urls import reverse
import os
from django.conf import settings
from admin.singleton_model import SingletonModel

class ShopSettings(SingletonModel):
  meta_h1 = models.CharField(max_length=250, null=True, blank=True, verbose_name="Заголовок первого уровня")
  meta_title = models.CharField(max_length=250, null=True, blank=True, verbose_name="META заголовок")
  meta_description = models.TextField(null=True, blank=True, verbose_name="META описание")
  meta_keywords = models.TextField(null=True, blank=True, verbose_name="META keywords")

# Категория
class Category(models.Model):
  name = models.CharField(max_length=150, db_index=True, unique=True, verbose_name="Название категории")
  slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name="URL")
  description = models.TextField(null=True, blank=True,  verbose_name="Описание категории")
  image = models.ImageField(upload_to="category_image", blank=True, null=True, verbose_name="Изображение категории")
  parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Дочерняя категория")
  meta_h1 = models.CharField(max_length=250, null=True, blank=True, verbose_name="Заголовок первого уровня")
  meta_title = models.CharField(max_length=250, null=True, blank=True, verbose_name="META заголовок")
  meta_description = models.TextField(null=True, blank=True, verbose_name="META описание")
  meta_keywords = models.TextField(null=True, blank=True, verbose_name="META keywords")
  add_menu = models.BooleanField(default=False, blank=True, null=True, verbose_name="Выводить в меню ? ")
  updated_at = models.DateTimeField(auto_now=True)
  
  class Meta:
    db_table = 'category' 
    verbose_name = 'Категория'
    verbose_name_plural = "Категории"
    
  def __str__(self):
    return self.name
  
  """ def get_absolute_url(self):
        return reverse("category_detail", kwargs={"category_path": self.slug}) """

  def get_absolute_url(self):
      parts = []
      current = self

      while current is not None:
          parts.append(current.slug)
          current = current.parent

      parts.reverse()

      category_path = "/".join(parts)

      return reverse("category_detail", kwargs={"category_path": category_path})


class Product(models.Model):
  STATUS_CHOICES = [
    ('published', 'Опубликовано'),
    ('draft', 'Черновик'),
    ('hidden', 'Скрыто'),
  ]

  name = models.CharField(max_length=150, db_index=True, verbose_name="Наименование")
  slug = models.SlugField(max_length=255, unique=True, blank=True, null=True, verbose_name="URL")
  category = models.ManyToManyField(Category, null=True, blank=True, verbose_name="Категории")
  image = models.ImageField(upload_to="product-image/", blank=True, null=True, verbose_name="Изображение товара")
  description = models.TextField(null=True, blank=True,  verbose_name="Описание категории")
  text = models.TextField(null=True, blank=True,  verbose_name="Текст на странице")
  meta_h1 = models.CharField(max_length=250, null=True, blank=True, verbose_name="Заголовок первого уровня")
  meta_title = models.CharField(max_length=250, null=True, blank=True, verbose_name="Мета заголовок")
  meta_description = models.TextField(null=True, blank=True, verbose_name="Meta описание")
  meta_keywords = models.TextField(null=True, blank=True, verbose_name="Meta keywords")
  updated_at = models.DateTimeField(auto_now=True)
  status = models.CharField(
    max_length=20,
    choices=STATUS_CHOICES,
    default='draft',
    verbose_name="Статус"
  )

  class Meta:
    db_table = 'product'
    verbose_name = 'Продукт'
    verbose_name_plural = "Продукты"
    ordering = ("-id",)

  def __str__(self):
    return f'{self.name}'

  """ Данный метод добавляет к id нули в начале """
  def display_id(self):
    return f'{self.id:05}' #self.id:05 - сделает так чтобы id состоял из 5 символов, если не хватате символов в начало добавить 0

  """ Данный метод возвращает цену со скидкой"""
  def sell_price(self):
    if self.sale:
      return round(self.price - self.price * self.sale / 100, 2)

    return self.price

  """ def get_absolute_url(self):
        return reverse("product", kwargs={"product_slug": self.slug}) """

  def get_absolute_url(self):
      category = self.category.first()
      if not category:
          return reverse("product", kwargs={
              "category_path": "",
              "product_slug": self.slug
          })

      parts = []
      current = category

      while current is not None:
          parts.append(current.slug)
          current = current.parent

      parts.reverse()
      category_path = "/".join(parts)

      return reverse("product", kwargs={
          "category_path": category_path,
          "product_slug": self.slug
      })

class Models(models.Model):
  STATUS_CHOICES = [
      ('published', 'Опубликовано'),
      ('draft', 'Черновик'),
      ('hidden', 'Скрыто'),
  ]

  parent = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="models_parent", verbose_name="Продукт")
  model = models.CharField(max_length=150, default="", db_index=True, verbose_name="Модель")
  power = models.CharField(max_length=150, blank=True, null=True, db_index=True, verbose_name="Мощность")
  el_network = models.CharField(max_length=150, blank=True, null=True,  db_index=True, verbose_name="Электрическая сеть")
  nom_capacity = models.CharField(max_length=150, blank=True, null=True, db_index=True, verbose_name="Ном. Производительность(м3/час)")
  max_capacity = models.CharField(max_length=150, blank=True, null=True,  db_index=True, verbose_name="Макс. Производительность(м3/час)")
  max_capacity_min = models.CharField(max_length=150, blank=True, null=True,  db_index=True, verbose_name="Макс. производительность (л/мин)")
  nom_head = models.CharField(max_length=150, blank=True, null=True, db_index=True, verbose_name="Номинальный напор(м)")
  max_head = models.CharField(max_length=150, blank=True, null=True, db_index=True, verbose_name="Максимальный напор (м)")
  suction_depth = models.CharField(max_length=150, blank=True, null=True, db_index=True, verbose_name="Максимальная глуб. всасывания(м)")
  сon_size = models.CharField(max_length=150, blank=True, null=True, db_index=True, verbose_name="Присоединительный размер (дюйм)")
  status = models.CharField(
      max_length=20,
      choices=STATUS_CHOICES,
      default='draft',
      verbose_name="Статус"
    )

class ProductImage(models.Model):
    parent = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images", verbose_name="Привязка к продукту")
    src = models.ImageField(upload_to="product-image/", null=True, blank=True, verbose_name="Дополнительны изображения")

    class Meta:
      verbose_name = 'Изображение'




