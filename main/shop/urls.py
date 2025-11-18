from django.urls import path

from shop import views


urlpatterns = [
    path('search/', views.catalog_search, name="catalog_search"),
    path('<path:category_path>/<slug:product_slug>/', views.product, name="product"),
    path('<path:category_path>/', views.category_detail, name="category_detail"),
    path('', views.category, name="category"),
]