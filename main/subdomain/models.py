from django.db import models

class Subdomain(models.Model):
  name = models.CharField(max_length=255, unique=True, verbose_name="Название поддомена")
  geotag = models.CharField(max_length=255, blank=True, null=True, verbose_name="ГеоТег")
  subdomain = models.CharField(max_length=255, unique=True, verbose_name="Субдомен")


class SubdomainContact(models.Model):
  phone = models.CharField(max_length=255, null=True, blank=True, verbose_name="Номер телефона")
  phone_two = models.CharField(max_length=255, null=True, blank=True, verbose_name="Второй номер телефона")
  time = models.CharField(max_length=255, null=True, blank=True, verbose_name="Режим работы")
  address = models.CharField(max_length=255, null=True, blank=True, verbose_name="Адрес компании")
  subdomain = models.ForeignKey(Subdomain, on_delete=models.CASCADE, related_name="contacts", verbose_name="Привязка к субдомену")