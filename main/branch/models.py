from django.db import models

class Branch(models.Model):
    STATUS_CHOICES = [
        ('published', 'Опубликовано'),
        ('draft', 'Черновик'),
        ('hidden', 'Скрыто'),
    ]

    title = models.CharField(max_length=250, blank=True, null=True, verbose_name="Офис")
    address = models.CharField(max_length=250, blank=True, null=True, verbose_name="Заголовок")
    phone_one = models.CharField(max_length=250, blank=True, null=True, verbose_name="Номер телефона")
    phone_two = models.CharField(max_length=250, blank=True, null=True, verbose_name="Номер телефона")
    email = models.EmailField(max_length=250, blank=True, null=True, db_index=True, verbose_name="Email")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name="Статус"
    )

    def __str__(self):
      return self.address


class Socials(models.Model):
  STATUS_CHOICES = [
    ('published', 'Опубликовано'),
    ('draft', 'Черновик'),
    ('hidden', 'Скрыто'),
  ]
  branch = models.ManyToManyField(Branch,related_name="socials",verbose_name="Филиалы")
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

  def __str__(self):
    return f"{self.name} ({self.branch})"