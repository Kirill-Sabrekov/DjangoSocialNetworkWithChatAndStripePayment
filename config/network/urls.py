from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.mainPage, name='mainPage'),
    path('new_post/', views.new_post, name='new_post'),
    path('new_post/submit/', views.submit),
    path('subscribe/<int:id>/', views.subscribe),
    path('unsubscribe/<int:id>/', views.unsubscribe),
    path('likes/<int:image_id>/<int:id>/', views.likes),
    path('dislikes/<int:image_id>/<int:id>/', views.dislikes),
    path('add_comment/<int:image_id>/', views.add_comment),
    path('userPage/<int:id>', views.userPage, name='userPage'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


