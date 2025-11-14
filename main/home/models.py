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

class ContactPage(SingletonModel):
  activate_page = models.BooleanField(default=False, verbose_name="Включить страницу")
  map = models.TextField(null=True, blank=True, verbose_name="Код карты")
  meta_h1 = models.CharField(max_length=250, blank=True, null=True, verbose_name="Заголовок первого уровня")
  meta_title = models.CharField(max_length=350, null=True, blank=True, verbose_name="Мета заголовок")
  meta_description = models.TextField(null=True, blank=True, verbose_name="Meta описание")
  meta_keywords = models.TextField(null=True, blank=True, verbose_name="Meta keywords")

class Socials(models.Model):
    STATUS_CHOICES = [
        ('published', 'Опубликовано'),
        ('draft', 'Черновик'),
        ('hidden', 'Скрыто'),
    ]

    name = models.CharField(max_length=250, blank=True, null=True, verbose_name="Название соц.сети")
    icon_white = models.FileField(upload_to="icons/", blank=True, null=True, verbose_name="Иконка светлая")
    icon_dark = models.FileField(upload_to="icons/", blank=True, null=True, verbose_name="Иконка темная")
    link = models.CharField(max_length=250, blank=True, null=True, verbose_name="Ссылка")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name="Статус"
    )

class SliderHero(models.Model):
    STATUS_CHOICES = [
        ('published', 'Опубликовано'),
        ('draft', 'Черновик'),
        ('hidden', 'Скрыто'),
    ]

    title = models.CharField(max_length=250, blank=True, null=True, verbose_name="Заголовок")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    icon_white = models.ImageField(upload_to="sliders/", blank=True, null=True, verbose_name="Изображение")
    link = models.CharField(max_length=250, blank=True, null=True, verbose_name="Ссылка")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name="Статус"
    )


class RobotsTxt(models.Model):
  content = models.TextField(default="User-agent: *\nDisallow: /admin/")
    
  def __str__(self):
    return "robots.txt"

