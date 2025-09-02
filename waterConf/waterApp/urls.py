from django.urls import path
from . import views

urlpatterns = [
    # Asosiy sahifalar
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('products/', views.products_view, name='products'),
    path('products/<int:product_id>/', views.product_detail_view, name='product_detail'),
    path('news/', views.news_view, name='news'),
    path('news/<int:news_id>/', views.news_detail_view, name='news_detail'),
    path('contact/', views.contact_view, name='contact'),
    path('faq/', views.faq_view, name='faq'),
    path('testimonials/', views.testimonials_view, name='testimonials'),

    # AJAX endpoints
    path('api/create-order/', views.create_order_ajax, name='create_order_ajax'),
    path('ajax/search/', views.search_products_ajax, name='search_products_ajax'),

    # API endpoints (ixtiyoriy)
    path('api/products/', views.api_products, name='api_products'),
    path('api/categories/', views.api_categories, name='api_categories'),
]