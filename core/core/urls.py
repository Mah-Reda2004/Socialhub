"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from posts import views as post_views
from account import views

urlpatterns = [
   
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('api/', include('posts.api_urls')),  # API JSON
    path('', post_views.post_list, name='home'),
    path('posts/', include('posts.urls')),# الصفحة الرئيسية
    
    path('post/<int:id>/delete/', post_views.post_delete, name='post_delete'),
    path("password-reset/", views.password_reset_request, name="password_reset_request"),
    path("password-reset/confirm/", views.password_reset_confirm, name="password_reset_confirm")

]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)