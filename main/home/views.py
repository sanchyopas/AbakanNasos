from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from home.models import *
from home.forms import *
from django.contrib import messages
from home.callback_send import email_callback

def order_form(request):
  if request.method == "POST":
    form = OrderForm(request.POST)
    if form.is_valid():
      name  = form.cleaned_data['name']
      phone = form.cleaned_data['phone']
      product = form.cleaned_data['product']
      title = 'Заказ обратного звонка'
      branch = form.cleaned_data['branch']
      recipient = branch.email

      mailTpl = "Заявка с сайта" + "\n\n" + "Имя: " +str(name) + "\n" + "Номер телефон: " + str(phone) + "\n" + "Насос: " + str(product) + "\n"
      if recipient:
        recipients = [recipient]
      else:
        recipients = [BaseSettings.objects.first().email]

      email_callback(mailTpl, title, recipients)

      return JsonResponse({"success": "success", "message": "Форма успешно отправлена !"})
    else:
      print(form)
  else:
    return JsonResponse({'status': "error", 'errors': form.errors})

  return JsonResponse({'status': 'error', 'mailTpl': 'Invalid request method'})

def callback_form(request):
  if request.method == "POST":
    form = CallbackForm(request.POST)

    if form.is_valid():
      name  = form.cleaned_data['name']
      phone = form.cleaned_data['phone']
      message = form.cleaned_data['message']
      title = 'Заказ обратного звонка'
      branch = form.cleaned_data['branch']
      recipient = branch.email

      mailTpl = "Обратный звонок" + "\n\n" + "Имя: " +str(name) + "\n" + "Номер телефон: " + str(phone) + "\n" + "Сообщение: " + str(message) + "\n"
      if recipient:
        recipients = [recipient]
      else:
        recipients = [BaseSettings.objects.first().email]

      email_callback(mailTpl, title, recipients)

      return JsonResponse({"success": "success", "message": "Форма успешно отправлена !"})
    else:
      print(form)
  else:
    return JsonResponse({'status': "error"})

  return JsonResponse({'status': 'error', 'mailTpl': 'Invalid request method'})

def contact_us_form(request):
  if request.method == "POST":
    form = contactUsForm(request.POST)

    if form.is_valid():
      name  = form.cleaned_data['name']
      phone = form.cleaned_data['phone']
      product = form.cleaned_data['product']
      branch = form.cleaned_data['branch']
      recipient = branch.email

      title = 'Заказ обратного звонка'

      mailTpl = "Связаться с нами" + "\n\n" + "Имя: " +str(name) + "\n" + "Номер телефон: " + str(phone) + "\n" + "Адрес филиала: " + str(product) + "\n"
      if recipient:
        recipients = [recipient]
      else:
        recipients = [BaseSettings.objects.first().email]

      email_callback(mailTpl, title, recipients)

      return JsonResponse({"success": "success", "message": "Форма успешно отправлена !"})
    else:
      print(form)
  else:
    return JsonResponse({'status': "error"})

  return JsonResponse({'status': 'error', 'mailTpl': 'Invalid request method'})

def index(request):
  try: 
    settings = HomeTemplate.objects.get()

  except:
    settings = HomeTemplate()

  about = AboutPage.objects.first()

  slides = SliderHero.objects.filter(status='published')
  category = Category.objects.filter(parent=None, status='published')
  slider_category = Category.objects.filter(parent=None, add_slider='published', status='published')

  context = {
    "settings": settings,
    "slides": slides,
    "category": category,
    "about": about,
    "slider_category": slider_category,
  }

  return render(request, 'pages/index.html', context)


def about(request):
  try:
    about = AboutPage.objects.get()
  except:
    about = AboutPage()

  context = {
    "about": about,
  }

  return render(request, 'pages/about.html', context)


def contact(request):
  try:
    contact = ContactPage.objects.get()
  except:
    contact = ContactPage()

  context = {
    "contact": contact,
  }

  return render(request, 'pages/contact.html', context)

def gallery(request):
  try:
    gallery = GalleryPage.objects.get()
  except:
    gallery = GalleryPage()

  items = GalleryItem.objects.filter(status="published")

  context = {
    "gallery": gallery,
    "items": items,
  }

  return render(request, 'pages/gallery.html', context)


def privacy(request):
  return render(request, "pages/privacy.html")

def cookie(request):
  return render(request, "pages/cookie.html")

def robots_txt(request):
  try:
      robots_txt = RobotsTxt.objects.first()  # Получаем первую запись, т.к. нам нужен только один robots.txt
      content = robots_txt.content if robots_txt else "User-agent: *\nDisallow: /admin/"
  except RobotsTxt.DoesNotExist:
    content = "User-agent: *\nDisallow: /admin/"

  return HttpResponse(content, content_type="text/plain")