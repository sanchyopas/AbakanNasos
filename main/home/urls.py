from django.urls import path

from home import views

urlpatterns = [
    path('privacy/', views.privacy, name="privacy"),
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),
    path('gallery/', views.gallery, name="gallery"),
    path('cookie/', views.cookie, name="cookie"),
    path('robots.txt', views.robots_txt),
    path('contact-form/', views.order_form, name="order_form"),
    path('callback-form/', views.callback_form, name="callback_form"),
    path('contact-us/', views.contact_us_form, name="contact_us_form"),

    path('', views.index, name="home"),
]