from django.urls import path
from reviews.views import *
from . import views

from reviews import admin

# from .views_new.product_views import admin_product, product_edit, product_add,product_delete


urlpatterns = [
    path('', views.admin, name="admin"),

    # Новые urls
    path('socials/', views.socials, name='socials'),
    path('socials/add/', views.socials_add, name='socials_add'),
    path('socials/<int:pk>/edit/', views.socials_edit, name='socials_edit'),
    path('socials/<int:pk>/delete/', views.socials_delete, name='socials_delete'),

    path('sliders/', views.sliders, name='sliders'),
    path('sliders/add/', views.sliders_add, name='sliders_add'),
    path('sliders/<int:pk>/edit/', views.sliders_edit, name='sliders_edit'),
    path('sliders/<int:pk>/delete/', views.sliders_delete, name='sliders_delete'),

    path('branch/', views.admin_branch, name='admin_branch'),
    path('branch/add/', views.branch_add, name='branch_add'),
    path('branch/<int:pk>/edit/', views.branch_edit, name='branch_edit'),
    path('branch/<int:pk>/delete/', views.branch_delete, name='branch_delete'),

    path('callback-block/', views.admin_callback_block, name='admin_callback_block'),
    path('home-page/', views.admin_home_page, name='admin_home_page'),
    path('admin-shop/', views.admin_shop, name='admin_shop'),

    #URl - отвечающие за отображение категорий, редактирование и удаление категории
    path('category/', views.admin_category, name='admin_category'),
    path('category/add/', views.category_add, name='category_add'),
    path('category/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('category/<int:pk>/delete/', views.category_delete, name='category_delete'),

    path('product/', views.admin_product, name='admin_product'),
    path('product/add/', views.product_add, name='product_add'),
    path('product/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('product/<int:pk>/delete/', views.product_delete, name='product_delete'),

    path('model/', views.admin_model, name='admin_model'),
    path('model/add/', views.model_add, name='model_add'),
    path('model/<int:pk>/edit/', views.model_edit, name='model_edit'),
    path('model/<int:pk>/delete/', views.model_delete, name='model_delete'),

    # Новые конец urls
    
    #URl - отвечающие за загрузку данных
    path('upload-goods/', views.upload_goods, name="upload_goods"),
    path('upload-succes/', views.upload_succes, name="upload-succes"),



    path('product/delete_properties/<int:pk>/', views.delete_properties, name='delete_properties'),

    #URl - отвечающие за отображение отзывов, редактирование и удаление отзывов
    path('admin-reviews/', admin.admin_reviews, name='admin_reviews'),
    path('admin-reviews/add/', admin.admin_reviews_add, name='admin_reviews_add'),
    path('admin-reviews/edit/<int:pk>/', admin.admin_reviews_edit, name='admin_reviews_edit'),
    path('admin_reviews/delete/<int:pk>/', admin.admin_reviews_delete, name='admin_reviews_delete'),
    
    #URl - отвечающие за отображение акций, редактирование и удаление акций
    path('stock/', views.admin_stock, name='admin_stock'),
    path('stock/add/', views.stock_add, name='stock_add'),
    path('stock/edit/<int:pk>/', views.stock_edit, name='stock_edit'),
    path('stock/delete/<int:pk>/', views.stock_delete, name='stock_delete'),
    
    #URl - отвечающие за отображение услуг, редактирование и удаление услуг
    path('service-page/', views.admin_service_page, name='admin_service_page'),
    path('serv/add/', views.service_add, name='service_add'),
    path('serv/edit/<int:pk>/', views.service_edit, name='service_edit'),
    path('serv/delete/<int:pk>/', views.service_delete, name='service_delete'),

    
    #URl - Шаблон общих настроек сайта
    path('settings/', views.admin_settings, name='admin_settings'),
    path('robots/', views.robots, name='robots'),
    

    path('prod-page/', views.admin_prod_page, name='admin_prod_page'),




    #URl - цвета памятников
    path('color-product/', views.admin_color, name='admin_color'),
    path('color-product/add/', views.admin_color_add, name='admin_color_add'),
    path('color-product/edit/<int:pk>/', views.admin_color_edit, name='admin_color_edit'),
    # path('subdomain/delete/<int:pk>/', views.subdomain_delete, name='subdomain_delete'),

    # Наши работы
    path('gallery-settings/', views.gallery_settings, name='gallery_settings'),
    path('gallery/add/', views.admin_gallery_add, name='admin_gallery_add'),
    path('gallery/edit/<int:pk>/', views.admin_gallery_edit, name='admin_gallery_edit'),
    path('gallery/delete/<int:pk>/', views.admin_gallery_delete, name='admin_gallery_delete'),

    path('work/add/', views.admin_work_add, name='admin_work_add'),
    path('work/edit/<int:pk>/', views.admin_work_edit, name='admin_work_edit'),
    path('work/delete/<int:pk>/', views.admin_work_delete, name='admin_work_delete'),
    
    #URl - отвечающие за отображение категории Галлереи, редактирование и удаление категории
    path('gallery-category/', views.admin_gallery_category, name='admin_gallery_category'),
    path('gallery-category/add/', views.gallery_category_add, name='gallery_category_add'),
    path('gallery-category/edit/<int:pk>/', views.gallery_category_edit, name='gallery_category_edit'),
    path('gallery-category/delete/<int:pk>/', views.gallery_category_delete, name='gallery_category_delete'),
    
    #URl - отвечающие за отображение категории Страниц блога, редактирование и удаление категории
    path('blog-settings/', views.blog_settings, name='blog_settings'),
    path('article/', views.article, name='article'),
    path('article/add/', views.article_add, name='article_add'),
    path('article/edit/<int:pk>/', views.article_edit, name='article_edit'),
    path('article/delete/<int:pk>/', views.article_delete, name='article_delete'),

    path('category-blog-settings/', views.category_blog_settings, name='category_blog_settings'),
    path('category-blog/', views.category_blog, name='category_blog'),
    path('category-blog/add/', views.category_blog_add, name='category_blog_add'),
    path('category-blog/edit/<int:pk>/', views.category_blog_edit, name='category_blog_edit'),
    path('category-blog/delete/<int:pk>/', views.category_blog_remove, name='category_blog_remove'),

]