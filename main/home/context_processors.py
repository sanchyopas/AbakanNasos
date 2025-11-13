from home.models import *
from shop.models import Category
from blog.models import BlogCategory
from service.models import Service
from reviews.models import Reviews

def socials(request):
    return {"socials": Socials.objects.filter(status='published')}
 
def load_settings(request):
    return {'site_settings': BaseSettings.load()}

def category_menu(request):
    return {'category_menu': Category.objects.all()}

def category_blog(request):
    return {'category_blog': BlogCategory.objects.all()}

def services(request):
    return {'services': Service.objects.filter(footer_view=True).order_by('-id')[:4]}


def reviews(request):
    return {'reviews': Reviews.objects.filter(status=True)}


def static_theme_path(request):
    from django.conf import settings
    return {'STATIC_THEME_PATH': settings.STATIC_THEME_PATH}