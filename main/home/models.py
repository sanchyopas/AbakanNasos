from django.db import models
from django.urls import reverse

from admin.singleton_model import SingletonModel

class BaseSettings(SingletonModel):
  logo = models.ImageField(upload_to="base-settings", blank=True, null=True, verbose_name="Логотип")
  logo_dark = models.ImageField(upload_to="base-settings", blank=True, null=True, verbose_name="Логотип Темный")
  logo_width = models.CharField(max_length=250, blank=True, null=True, db_index=True, verbose_name="Ширина")
  logo_height = models.CharField(max_length=250, blank=True, null=True, db_index=True, verbose_name="Высота")
  phone = models.CharField(max_length=50, blank=True, null=True, db_index=True, verbose_name="Номер телефона")
  time_work = models.CharField(max_length=250, blank=True, null=True, db_index=True, verbose_name="Время работы")
  email = models.EmailField(max_length=250, blank=True, null=True, db_index=True, verbose_name="Email")
  address = models.CharField(max_length=250, blank=True, null=True, verbose_name="Адрес")
  meta_h1 = models.CharField(max_length=350, null=True, blank=True, verbose_name="Заголовок первого уровня")
  meta_title = models.CharField(max_length=350, null=True, blank=True, verbose_name="Мета заголовок")
  meta_description = models.TextField(null=True, blank=True, verbose_name="Meta описание")
  meta_keywords = models.TextField(null=True, blank=True, verbose_name="Meta keywords")
  favicon = models.FileField(upload_to='base-settings/', blank=True, null=True, verbose_name="ФавИконка")
  

class HomeTemplate(SingletonModel):
  banner = models.ImageField(upload_to="home-page", blank=True, null=True, verbose_name="Картинка главной страницы")
  meta_h1 = models.CharField(max_length=250, blank=True, null=True, verbose_name="Заголовок первого уровня")
  meta_title = models.CharField(max_length=350, null=True, blank=True, verbose_name="Мета заголовок")
  meta_description = models.TextField(null=True, blank=True, verbose_name="Meta описание")
  meta_keywords = models.TextField(null=True, blank=True, verbose_name="Meta keywords")
  sale_text = models.CharField(max_length=250, blank=True, null=True, verbose_name="Текст скидки в всплывающем окне")

class ContactTemplate(SingletonModel):
  activate_page = models.BooleanField(default=False, verbose_name="Включить страницу")
  map = models.TextField(null=True, blank=True, verbose_name="Код карты")
  meta_h1 = models.CharField(max_length=250, blank=True, null=True, verbose_name="Заголовок первого уровня")
  meta_title = models.CharField(max_length=350, null=True, blank=True, verbose_name="Мета заголовок")
  meta_description = models.TextField(null=True, blank=True, verbose_name="Meta описание")
  meta_keywords = models.TextField(null=True, blank=True, verbose_name="Meta keywords")


  
class Stock(models.Model):
  """Model"""
  title = models.CharField(max_length=250, blank=True, null=True, verbose_name="Название акции")
  description = models.TextField(blank=True, null=True, verbose_name="Описание акции")
  validity = models.DateTimeField(blank=True, null=True, help_text="После окончания акции, она перейдет в состояние не активна", verbose_name="Срок дейстия акции")
  status = models.BooleanField(default=True, verbose_name="Статус публикации")
  image = models.ImageField(upload_to="stock", null=True, blank=True, verbose_name="ФОтография акции")
  slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name="URL")
  meta_title = models.CharField(max_length=350, null=True, blank=True, verbose_name="Мета заголовок")
  meta_description = models.TextField(null=True, blank=True, verbose_name="Meta описание")
  meta_keywords = models.TextField(null=True, blank=True, verbose_name="Meta keywords")
  slider_status = models.BooleanField(default=False, verbose_name="Слайдер на главной")

  def get_absolute_url(self):
      return reverse("stock_detail", kwargs={"slug": self.slug})
    
class GalleryCategory(models.Model):
  name = models.CharField(max_length=250, null=True, blank=True, verbose_name="Наименование")
  meta_h1 = models.CharField(max_length=350, null=True, blank=True, verbose_name="Заголовок первого уровня")
  meta_title = models.CharField(max_length=350, null=True, blank=True, verbose_name="Мета заголовок")
  meta_description = models.TextField(null=True, blank=True, verbose_name="Meta описание")
  meta_keywords = models.TextField(null=True, blank=True, verbose_name="Meta keywords")
  slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name="")
  home_view = models.BooleanField(default=False, verbose_name="Отображать на главной ?")
  image = models.ImageField(upload_to="gallery-category", null=True, blank=True, verbose_name="Фотография категории")
  
  def __str__(self):
    return self.name
  
  def get_absolute_url(self):
    return reverse("gal_cat_detail", kwargs={"slug": self.slug})
  
class Gallery(models.Model):
  image = models.ImageField(upload_to="gallery-image", null=True, blank=True, verbose_name="Фотография")
  name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Наименование пойдет в alt и title")
  is_active = models.BooleanField(default=True, verbose_name="Выводить на сайт ?")
  
  def __str__(self):
    return self.name

class Works(models.Model):
  image = models.ImageField(upload_to="gallery-image", null=True, blank=True, verbose_name="Фотография")
  name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Название")
  text = models.TextField( null=True, blank=True, verbose_name="Минимальный текст")
  is_active = models.BooleanField(default=True, verbose_name="Выводить на сайт ?")

class RobotsTxt(models.Model):
  content = models.TextField(default="User-agent: *\nDisallow: /admin/")
    
  def __str__(self):
    return "robots.txt"

class About(models.Model):
  description = models.TextField(blank=True, null=True, verbose_name="Первый текст")
  description_two = models.TextField(blank=True, null=True, verbose_name="Второй текст")
  image = models.ImageField(upload_to="about", null=True, blank=True, verbose_name="Изображение")
  meta_h1 = models.CharField(max_length=350, null=True, blank=True, verbose_name="Заголовок первого уровня")
  meta_title = models.CharField(max_length=350, null=True, blank=True, verbose_name="Мета заголовок")
  meta_description = models.TextField(null=True, blank=True, verbose_name="Meta описание")
  meta_keywords = models.TextField(null=True, blank=True, verbose_name="Meta keywords")

class Production(models.Model):
  meta_h1 = models.CharField(max_length=350, null=True, blank=True, verbose_name="Заголовок первого уровня")
  meta_title = models.CharField(max_length=350, null=True, blank=True, verbose_name="Мета заголовок")
  meta_description = models.TextField(null=True, blank=True, verbose_name="Meta описание")
  meta_keywords = models.TextField(null=True, blank=True, verbose_name="Meta keywords")
  sale_text = models.CharField(max_length=250, blank=True, null=True, verbose_name="Текст скидки в всплывающем окне")

class Delivery(models.Model):
  description = models.TextField(blank=True, null=True, verbose_name="Текст на странице")
  description_two = models.TextField(blank=True, null=True, verbose_name="Второй текст на странице")
  meta_h1 = models.CharField(max_length=350, null=True, blank=True, verbose_name="Заголовок первого уровня")
  meta_title = models.CharField(max_length=350, null=True, blank=True, verbose_name="Мета заголовок")
  meta_description = models.TextField(null=True, blank=True, verbose_name="Meta описание")
  meta_keywords = models.TextField(null=True, blank=True, verbose_name="Meta keywords")

class SalesOffices(models.Model):
  name = models.CharField(max_length=250, null=True, blank=True, verbose_name="Наименование", default="Офис продаж Максимум")
  address = models.CharField(max_length=250, null=True, blank=True, verbose_name="Адрес")
  phone = models.CharField(max_length=250, null=True, blank=True, verbose_name="Номер телефона")
  time_work = models.CharField(max_length=250, null=True, blank=True, verbose_name="Режим работы", default="Вт-сб 09:00-18:00, Вс-пн выходной")
