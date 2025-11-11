from django.urls import path

from blog import views

urlpatterns = [
    path('', views.blog, name="blog"),
    path('<slug:category_slug>/', views.category_post, name='category_post'),
    path('<slug:category_slug>/<slug:slug>/', views.post, name="post"),
]