from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from home.models import BaseSettings, Production, Works, About, Gallery, GalleryCategory, HomeTemplate, RobotsTxt, Stock, Delivery, ContactTemplate
from cart.models import Cart
from home.forms import CallbackForm,OknaForm, ContactForm, OrderForm, ReviewsPopupForm
from home.callback_send import email_callback
from blog.models import Post
from shop.models import Category, Product
from reviews.models import Reviews
from django.http import JsonResponse
from django.db.models import Q

def callback(request):
  if request.method == "POST":
    form = CallbackForm(request.POST)
    if form.is_valid():
      name  = form.cleaned_data['name']
      phone = form.cleaned_data['phone']

      title = 'Заказ обратного звонка'
      messages = "Заказ обратного звонка:" + "\n" + "Имя: " +str(name) + "\n" + "Номер телефона: " + str(phone) + "\n"

      email_callback(messages, title)

      return JsonResponse({"success": "success"})
    else:
      return JsonResponse({'status': "error", 'errors': form.errors})

  return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def order_form(request):
  if request.method == "POST":
    form = OrderForm(request.POST)
    if form.is_valid():
      name  = form.cleaned_data['name']
      phone = form.cleaned_data['phone']
      product = form.cleaned_data['product']

      title = 'Заявка с заказом'
      messages = "Заявка с заказом:" + "\n" + "Имя: " +str(name) + "\n" + "Номер телефона: " + str(phone) + "\n" + "Товар: " + str(product) + "\n"

      email_callback(messages, title)

      return JsonResponse({"success": "success"})
    else:
      return JsonResponse({'status': "error", 'errors': form.errors})

  return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def contact_form(request):
  if request.method == "POST":
    form = ContactForm(request.POST)
    if form.is_valid():
      name  = form.cleaned_data['name']
      phone = form.cleaned_data['phone']
      title = 'Заказ обратного звонка'
      messages = "Заказ обратного звонка:" + "\n" + "Имя: " +str(name) + "\n" + "Номер телефона: " + str(phone) + "\n"

      email_callback(messages, title)

      return JsonResponse({"success": "success"})
    else:
      return JsonResponse({'status': "error", 'errors': form.errors})

  return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def okna_form(request):
   if request.method == "POST":
      form = OknaForm(request.POST)
      if form.is_valid():
        name  = form.cleaned_data['name']
        phone = form.cleaned_data['phone']
        page_name = form.cleaned_data['page_name']
        title = 'Форма получения скидки'
        messages = "Форма получения скидки:" + "\n" + "Имя: " +str(name) + "\n" + "Номер телефона: " + str(phone) + "\n" + "Скидка: " + str(page_name)

        email_callback(messages, title)

        return JsonResponse({"success": "success"})
      else:
        return JsonResponse({'status': "error", 'errors': form.errors})

   return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def index(request):
  try: 
    home_page = HomeTemplate.objects.get()
  except:
    home_page = HomeTemplate.objects.all()

  products = Product.objects.filter(status=True)[:4]
  posts = Post.objects.filter(status=True)
  text_sale = home_page.sale_text

  context = {
    "home_page": home_page,
    "products": products,
    "posts": posts,
  }

  if text_sale:
    context["page_name"] = "home"
    context["text_sale"] = text_sale

  return render(request, 'pages/index.html', context)

def about(request):
  try:
    about_page = About.objects.get()
  except:
    about_page = About()


  context = {
    "about_page": about_page
  }

  return render(request, "pages/about.html", context)


def contact(request):
  try:
    contact_page = ContactTemplate.objects.get()
  except:
    contact_page = ContactTemplate()


  context = {
    "contact_page": contact_page
  }

  return render(request, "pages/contact.html", context)


def production(request):
  try:
    settings = Production.objects.get()
  except:
    settings = Production()

  text_sale = settings.sale_text

  context = {
    "settings": settings,
  }

  if text_sale:
    context["page_name"] = "okna"
    context["text_sale"] = text_sale

  return render(request, "pages/production.html", context)

def works(request):
    try:
      work_page = GalleryCategory.objects.get()
    except:
      work_page = GalleryCategory()

    works = Gallery.objects.filter(is_active=True)
    works_list = Works.objects.filter(is_active=True)
    context = {
      "work_page": work_page,
      "works": works,
      "works_list":works_list
    }

    return render(request, "pages/works.html", context)

def delivery(request):
  try:
    delivery_page = Delivery.objects.get()
  except:
    delivery_page = Delivery()

  context = {
    "delivery_page": delivery_page,
  }
  return render(request, "pages/delivery.html", context)

def politika(request):
  return render(request, "pages/politika.html")

def cookie(request):
  return render(request, "pages/cookie.html")

def robots_txt(request):
  try:
      robots_txt = RobotsTxt.objects.first()  # Получаем первую запись, т.к. нам нужен только один robots.txt
      content = robots_txt.content if robots_txt else "User-agent: *\nDisallow: /admin/"
  except RobotsTxt.DoesNotExist:
    content = "User-agent: *\nDisallow: /admin/"

  return HttpResponse(content, content_type="text/plain")