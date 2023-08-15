"""
URL configuration for socialnet project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from core.views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage),
    path('contacts/', contacts),
    path('about_us/', about_us),
    path('posts/<int:id>/', post_detail),
    path('profile/<int:id>/', profile_detail, name='profile'),
    path('category_info/', category_list),
    path('category_info/<int:id>/', category_detail),
    path('short_video/<int:id>/', short_video, name='short-info'),
    path('short_lst/', short_list, name='shorts-list'),
    path('saved_post_list/', saved_post_list, name='saved_post_list'),
    path('<int:user_id>/', user_post, name='user_posts'),
    path('posts/', post_list, name='posts'),
    path('add-post/', create_post, name='add-post'),
    path('add-short/', add_short, name='add-short'),
    path('add-saved/', add_saved, name='add-saved'),
    path('remove-saved/', remove_saved, name='remove-saved'),
    path('registration/', register, name='register'),
    path('users/', include('userapp.urls')),
    path('search/', search, name='search'),
    path('search-result/', search_result, name='search-result'),
    path('add-subscriber/<int:profile_id>/', add_subscriber, name='add-subscriber'),




]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)