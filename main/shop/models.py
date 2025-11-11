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
  sale_text = models.CharField(max_length=250, blank=True, null=True, verbose_name="Текст скидки в всплывающем окне")
  updated_at = models.DateTimeField(auto_now=True)
  
  class Meta:
    db_table = 'category' 
    verbose_name = 'Категория'
    verbose_name_plural = "Категории"
    
  def __str__(self):
    return self.name
  
  def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug})

# Продукт
class Product(models.Model):
  article = models.CharField(max_length=255, blank=True, null=True, verbose_name="Артикул")
  name = models.CharField(max_length=150, db_index=True, verbose_name="Наименование")
  slug = models.SlugField(max_length=255, unique=True, blank=True, null=True, verbose_name="URL")
  category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='main_products', null=True, blank=True)
#   categories = models.ManyToManyField(Category, related_name='related_products', blank=True, verbose_name="Категории")
  manufacturer = models.CharField(max_length=250, db_index=True, null=True, blank=True, verbose_name="Производитель")
  manufacturer_description = models.TextField(blank=True, null=True, verbose_name="Описание производителя")
  colors = models.CharField(max_length=250, null=True, blank=True, verbose_name="Цветовая схема")
  image = models.ImageField(upload_to="product_iamge", blank=True, null=True, verbose_name="Изображение товара")
  price = models.CharField(max_length=250, db_index=True, null=True, blank=True, verbose_name="Цена")
  installment = models.CharField(max_length=50, blank=True, null=True, verbose_name="Рассрочка")
  sale = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Скидка")
  quantity = models.PositiveIntegerField(default=0, verbose_name="Количество")
  quantity_purchase = models.IntegerField(default=0, verbose_name="Количество купленных")
  status = models.BooleanField(default=True, verbose_name="Опубликовать ?")
  meta_h1 = models.CharField(max_length=250, null=True, blank=True, verbose_name="Заголовок первого уровня")
  meta_title = models.CharField(max_length=250, null=True, blank=True, verbose_name="Мета заголовок")
  meta_description = models.TextField(null=True, blank=True, verbose_name="Meta описание")
  meta_keywords = models.TextField(null=True, blank=True, verbose_name="Meta keywords")
  updated_at = models.DateTimeField(auto_now=True)


  class Meta:
    db_table = 'product'
    verbose_name = 'Продукт'
    verbose_name_plural = "Продукты"
    ordering = ("-id",)

  def __str__(self):
    return f'{self.name} Кол-во - {self.quantity}'

  """ Данный метод добавляет к id нули в начале """
  def display_id(self):
    return f'{self.id:05}' #self.id:05 - сделает так чтобы id состоял из 5 символов, если не хватате символов в начало добавить 0

  """ Данный метод возвращает цену со скидкой"""
  def sell_price(self):
    if self.sale:
      return round(self.price - self.price * self.sale / 100, 2)

    return self.price

  def get_absolute_url(self):
        return reverse("product", kwargs={"slug": self.slug})

""" Характеристики товара """
class Properties(models.Model):
    parent =  models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name="properties", verbose_name='Родитель')
    name = models.CharField(max_length=250, null=True, blank=True, verbose_name="Название характеристки")
    value = models.CharField(max_length=250, null=True, blank=True, verbose_name="Значение характеристки")

    def __str__(self):
      return self.name

class ProductImage(models.Model):
    parent = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images", verbose_name="Привязка к продукту")
    src = models.ImageField(upload_to="product_iamge", null=True, blank=True, verbose_name="Дополнительны изображения")

    class Meta:
      verbose_name = 'Изображение'


        
class ColorProduct(models.Model):
  name = models.CharField(max_length=250, unique=True, null=True, blank=True, verbose_name="Название цвета")
  code_color = models.CharField(max_length=250, unique=True, null=True, blank=True, verbose_name="Код цвета")
  image_color = models.ImageField(upload_to="product_color", null=True, blank=True, verbose_name="Изображение цвета")
  active = models.BooleanField(default=True, verbose_name="Выводить на сайте")



