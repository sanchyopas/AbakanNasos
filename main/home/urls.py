from django.urls import path

from home import views

urlpatterns = [
    path("o-nas/", views.about, name="about"),
    path("production/", views.production, name="production"),
    path("works/", views.works, name="works"),
    path('contacts/', views.contact, name="contact"),
#     path('akcii/', views.stock, name="stock"),
#     path('akcii/<slug:slug>', views.stock_detail, name="stock_detail"),
#     path('gallery/', views.gallery, name="gallery"),
#     path('gallery-category/<slug:slug>/', views.gal_cat_detail, name="gal_cat_detail"),
    path('delivery/', views.delivery, name="delivery"),
    path('politika/', views.politika, name="politika"),
    path('cookie/', views.cookie, name="cookie"),
    path('callback/', views.callback, name="callback"),
    path('contact-form/', views.contact_form, name="contact_form"),
    path('okna-form/', views.okna_form, name="okna_form"),
    path('order-form/', views.order_form, name="order_form"),
#     path('consultation/', views.consultation, name="consultation"),
#     path('stock-product/', views.stock_product, name="stock_product"),
    path('robots.txt', views.robots_txt),
    # path('uslugi/', views.about, name="about"),
    # path('valancy/', views.about, name="about"),
    
    path('', views.index, name="home"),
]