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

def post_list(request):
    context = {}
    post_list = Post.objects.all()
    context['posts'] = post_list
    return render(request, 'post_lst.html', context)


def saved_post_list(request):
    posts = Post.objects.filter(saved_posts__user=request.user)
    context = {'posts': posts}
    return render(request, 'saved_post_list.html', context)



def profile_detail(request, id):
    context = {}
    context['profile'] = Profile.objects.get(id=id)
    return render(request, 'profile_detail.html', context)

def user_post(request, user_id):
    user = User.objects.get(id=user_id)
    posts = Post.objects.filter(creator=user)
    context = {
        'user': user,
        'posts': posts
    }
    return render(request, 'user_posts.html', context)

def category_detail(request, id):
    context = {}
    category_info = Category.objects.get(id=id)
    context['category'] = category_info
    return render(request, 'category_info.html', context)

def category_list(request):
    context = {}
    category_info = Category.objects.all()
    context['category'] = category_info
    return render(request, 'category_lst.html', context)


def short_video(request):
    short_video_object = Short.objects.all()
    return render(request, 'short_video.html', {'short_video_object': short_video_object})

def short_list(request):
    short_lst = Short.objects.get(id=id)
    return render(request, 'short_lst.html', {'short_lst': short_lst})


def contacts(request):
    return HttpResponse("Наши контакты")


def about_us(request):
    return HttpResponse("Информация о нас!")
