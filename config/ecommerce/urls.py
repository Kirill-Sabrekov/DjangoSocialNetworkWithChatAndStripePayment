from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.new_purchase, name='ecommerce'),
    path('cart/', views.cart, name='cart'),
    path('order/', views.order, name='order'),
    path('finished_order/', views.finished_order, name='finished_order'),

    path('config/', views.stripe_config),  
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'), 
    path('success', views.success_view), 
    path('cancelled', views.cancelled_view), 
    path('webhook/', views.stripe_webhook), 
    path('create-product/', views.create_product),
] #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
