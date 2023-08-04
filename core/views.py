from django.shortcuts import render, HttpResponse
from .models import *


# Create your views here.
def homepage(request):
    context = {}
    context['name'] = 'JE'
    posts_list = Post.objects.all()
    context['posts'] = posts_list
    return render(request, 'home.html', context)


def post_detail(request, id):
    context = {}
    post_object = Post.objects.get(id=id)
    context['post'] = post_object
    return render(request, 'post_info.html', context)


def profile_detail(request, id):
    context = {}
    context['profile'] = Profile.objects.get(id=id)
    return render(request, 'profile_detail.html', context)


def category_detail(request, id):
    context = {}
    category_info = Category.objects.get(id=id)
    context['category'] = category_info
    return render(request, 'category_info.html', context)


# def (request, id):
#     category_info = Category.objects.get(id=id)
#     return render(request, 'category_info.html', {'category_info': category_info})


def short_video(request):
    short_video_object = Short.objects.all()
    return render(request, 'short_video.html', {'short_video_object': short_video_object})


def contacts(request):
    return HttpResponse("Наши контакты")


def about_us(request):
    return HttpResponse("Информация о нас!")
