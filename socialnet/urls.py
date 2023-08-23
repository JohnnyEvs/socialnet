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
    path('posts-list-cbv/', PostListView.as_view(), name='posts-list-cbv'),
    path('posts-list-filter/', PostListFilterView.as_view(), name='posts-list-filter'),
    path('posts-cbv/<int:id>/', PostDetailView.as_view(), name='post-detail-cbv'),
    path('profile/<int:id>/', profile_detail, name='profile'),
    path('category_info/', category_list),
    path('category_info/<int:id>/', category_detail),
    path('short_video-cvb/<int:pk>/', Short_videoView.as_view(), name='short-info-cvb'),
    path('short-lst-cvb/', Short_listView.as_view(), name='shorts-list-cvb'),
    path('shorts-filter/', ShortsFilterView.as_view(), name='shorts-filter'),
    path('saved_post_list/', saved_post_list, name='saved_post_list'),
    path('update-short/<int:id>/', update_short, name='update-short'),
    path('<int:user_id>/', user_post, name='user_posts'),
    path('posts/', post_list, name='posts'),
    path('add-post/', create_post, name='add-post'),
    path('update-post/<int:id>/', update_post, name='update-post'),
    path('delete-post/<int:id>/', delete_post, name='delete-post'),
    path('add-post-form/', add_post_form, name='add-post-form'),
    path('edit-comment/<int:id>/', edit_comment, name='edit-comment'),
    path('delete-comment/<int:id>/', delete_comment, name='delete-comment'),
    path('add-short/', add_short, name='add-short'),
    path('add-saved/', add_saved, name='add-saved'),
    path('remove-saved/', remove_saved, name='remove-saved'),
    path('registration/', register, name='register'),
    path('users/', include('userapp.urls')),
    path('search-cvb/', SearchView.as_view(), name='search-cvb'),
    path('search-result-cvb/', Search_resultView.as_view, name='search-result-cvb'),
    path('add-subscriber/<int:profile_id>/', add_subscriber, name='add-subscriber'),
    path('subcsribes/<int:profile_id>/', SubcsribesView.as_view(), name='subcsribes'),
    path('remove-follower/<int:profile_id>/', remove_follower, name='remove-follower'),
    path('note_lst/', show_notification, name='note_lst'),
    path('note_lst_cvb/', Show_notificationView.as_view(), name='note_lst_cvb'),
    path('add-profile/', add_profile, name='add-profile'),
    path('edit-profile/<int:id>/', edit_profile, name='edit-profile'),
    path('about/', AboutView.as_view(), name='about'),
    path('contactsus/', ContactsusView.as_view(), name='contactsus'),
    path('faq/', FAQView.as_view(), name='faq'),
    path('stuff/', StuffView.as_view(), name='stuff'),





]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)