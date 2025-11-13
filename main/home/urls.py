from django.urls import path

from home import views

urlpatterns = [
    path('politika/', views.politika, name="politika"),
    path('cookie/', views.cookie, name="cookie"),
    path('robots.txt', views.robots_txt),

    path('', views.index, name="home"),
]