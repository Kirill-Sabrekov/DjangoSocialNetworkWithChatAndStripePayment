from django.contrib import admin
from django.urls import path, include
from users.views import account_signup_view, account_login_view
from config.views import home_page
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page, name='home'),
    path("accounts/signup/", view=account_signup_view, name='account_signup'),
    path("accounts/login/", view=account_login_view, name='account_login'),
    path('accounts/', include('allauth.urls')),
    path("chat/", include('chat.urls')),
    path('mainPage/', include('network.urls')),
    path('ecommerce/', include('ecommerce.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
