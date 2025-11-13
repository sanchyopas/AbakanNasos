from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from home.models import *
from home.forms import *
from home.callback_send import email_callback


def index(request):
  try: 
    settings = HomeTemplate.objects.get()
  except:
      settings = HomeTemplate.objects.all()

  context = {
    "settings": settings,
  }

  return render(request, 'pages/index.html', context)



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