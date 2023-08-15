from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from .models import *
from .forms import CommentForm, RegistrationUserForm


# Create your views here.
def homepage(request):
    context = {}
    posts_list = Post.objects.all()
    context['posts'] = posts_list
    short_list = Short.objects.all()
    context['shorts'] = short_list
    return render(request, 'home.html', context)


def post_detail(request, id):
    context = {}
    post_object = Post.objects.get(id=id)
    context['post'] = post_object
    comment_form = CommentForm()
    context['comment_form'] = comment_form
    comments_list = Comment.objects.filter(post=post_object)
    context['comments'] = comments_list
    if request.method == "GET":
        return render(request, 'post_info.html', context)
    elif request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.created_by = request.user
            new_comment.post = post_object
            new_comment.save()
            return HttpResponse('done')

def add_saved(request):
    if request.method == "POST":
        post_id = request.POST['post_id']
        post_object = Post.objects.get(id=post_id)
        saved_post, created = SavedPosts.objects.get_or_create(user=request.user)
        saved_post.post.add(post_object)
        saved_post.save()
        return redirect('/saved_post_list/')

def remove_saved(request):
    if request.method == "POST":
        post_id = request.POST['post_id']
        post_object = Post.objects.get(id=post_id)
        saved_post = SavedPosts.objects.get(user=request.user)
        saved_post.post.remove(post_object)
        saved_post.save()
        return redirect('/saved_post_list/')

def add_subscriber(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    profile.subscriber.add(request.user)
    profile.save()
    messages.success(request, 'You are one of us')
    return redirect(f'/profile/{profile.id}/')

def remove_follower(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    profile.subscriber.remove(profile_id)
    profile.save()
    messages.success(request, 'You are not follower')
    return redirect(f'/profile/{profile.id}')


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
    profile = Profile.objects.get(id=id)
    context['profile'] = profile
    user_posts = Post.objects.filter(creator=profile.user)
    context['user_posts'] = user_posts
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


@login_required(login_url='users/sign-in/')
def add_short(request):
    if request.method == "GET":
        return render(request, 'short_form.html')
    elif request.method == "POST":
        new_short_object = Short(
            user=request.user,
            video=request.FILES['video_file'],
        )
        new_short_object.save()
        return redirect('short-info', id=new_short_object.id)

def short_video(request, id):
    short_video_object = Short.objects.get(id=id)
    return render(request, 'short_video.html', {'short': short_video_object})


def short_list(request):
    short_lst = Short.objects.all()
    return render(request, 'short_lst.html', {'short_lst': short_lst})


def create_post(request):
    if request.method == "GET":
        return render(request, 'create_post_form.html')
    elif request.method == "POST":
        data = request.POST
        print(data)
        new_post = Post()
        new_post.name = data['post_name']
        new_post.description = data['description']
        new_post.photo = request.FILES['photo']
        new_post.creator = request.user
        new_post.save()
        return HttpResponse('done')

def search(request):
    return render(request, 'search.html')

def search_result(request):
    key_word = request.GET['key_word']
    # posts = Post.objects.filter(name__icontains=key_word)
    posts = Post.objects.filter(
        Q(name__icontains=key_word) |
        Q(description__icontains=key_word)
    )
    context = {'posts': posts}
    return render(request, 'home.html', context)

def contacts(request):
    return HttpResponse("Наши контакты")


def about_us(request):
    return HttpResponse("Информация о нас!")


def register(request):
    if request.method == "POST":
        form = RegistrationUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('/')
            # return HttpResponse('You are the chosen one')
    else:
        form = RegistrationUserForm()
    return render(request, 'registration.html', {'form': form})
