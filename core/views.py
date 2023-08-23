from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django_filters.views import FilterView
from django.views import View
from .models import *
from .forms import *
from .filters import *


# Create your views here.
class NoContextView(View):
    template_name = None
    def get(self, request):
        return render(request, self.template_name)
class AboutView(NoContextView):
    template_name = 'about.html'

class FAQView(NoContextView):
    template_name = 'faq.html'

class StuffView(NoContextView):
    template_name = 'stuff.html'

class ContactsusView(NoContextView):
    template_name = 'contactsus.html'


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
        if 'like' in request.POST:
            post_object.likes += 1
            post_object.save()
            Notification.objects.create(
                user=post_object.creator,
                text=f'{request.user.username} likes your post {post_object.id}'
            )
        elif 'dislike' in request.POST:
            post_object.likes -= 1
            post_object.save()
            Notification.objects.create(
                user=post_object.creator,
                text=f'{request.user.username} dislikes your post {post_object.id}'
            )
            return redirect(post_detail, id=id)
        else:
            comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
           new_comment = comment_form.save(commit=False)
           new_comment.created_by = request.user
           new_comment.post = post_object
           new_comment.save()
           Notification.objects.create(
               user=post_object.creator,
               text=f'{request.user.username} Commented your post {post_object.id}'
           )
        return redirect(post_detail, id=id)

class PostDetailView(View):
    def get_context(self):
        id = self.kwargs['id']
        context = {}
        post_object = Post.objects.get(id=id)
        context['post'] = post_object
        comment_form = CommentForm()
        context['comment_form'] = comment_form
        comments_list = Comment.objects.filter(post=post_object)
        context['comments'] = comments_list
        return context


    def get(self, request, *args, **kwargs):
        context = self.get_context()
        return render(request, 'post_info.html', context)

    def post(self, request, *args, **kwargs):
        context = context = self.get_context()
        post_object = context['post']
        if 'like' in request.POST:
            post_object.likes += 1
            post_object.save()
            Notification.objects.create(
                user=post_object.creator,
                text=f'{request.user.username} likes your post {post_object.id}'
            )
        elif 'dislike' in request.POST:
            post_object.likes -= 1
            post_object.save()
            Notification.objects.create(
                user=post_object.creator,
                text=f'{request.user.username} dislikes your post {post_object.id}'
            )
        else:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.created_by = request.user
                new_comment.post = post_object
                new_comment.save()
                Notification.objects.create(
                    user=post_object.creator,
                    text=f'{request.user.username} Commented your post {post_object.id}'
                )
        return redirect('post-detail-cbv', id=post_object.id)


def edit_comment(request, id):
    comment = Comment.objects.get(id=id)
    if request.user != comment.created_by:
        return redirect(post_detail)
    if request.method == 'POST':
        form = CommentForm(
            data=request.POST,
            instance=comment
        )
        if form.is_valid():
            form.save()
            return redirect(post_detail, id=comment.post.id)
    form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'edit_comment.html', context)


def delete_comment(request, id):
    comment = Comment.objects.get(id=id)
    if request.user != comment.created_by:
        return redirect(post_detail)
    comment.delete()
    return redirect(post_detail, id=comment.post.id)


class SubcsribesView(View):
    def get(self, request, *args, **kwargs):
        user_object = User.objects.get(id=kwargs['user_id'])
        profiles_list = user_object.followed_user_profile.all()
        context = {'profiles_list': profiles_list}
        return render(request, 'subscribes.html', context)


def add_profile(request):
    profile_form = ProfileForm()
    context = {'profile_form': profile_form}
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            profile_object = profile_form.save(commit=False)
            profile_object.user = request.user
            profile_object.save()
            return redirect(profile_detail, id=profile_object.id)
        else:
            return HttpResponse('Not valid')
    return render(request, 'add_profile.html', context)


def edit_profile(request, id):
    profile = Profile.objects.get(id=id)
    profile_form = ProfileForm(
        instance=profile
    )
    context = {'profile_form': profile_form}
    if request.method == 'POST':
        profile_form = ProfileForm(instance=profile, data=request.POST, files=request.FILES)
        if profile_form.is_valid():
            profile_form.save()
            return redirect(profile_detail, id=profile.id)
    return render(request, 'update_profile.html', context)




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
    new_notification = Notification(
        user = profile.user,
        text = f'user {request.user.username} follow you'
    )
    new_notification.save()
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

class PostListView(ListView):
    queryset = Post.objects.all()
    template_name = 'posts-list-cbv.html'

class PostListFilterView(FilterView):
    model = Post
    filterset_class = PostFilters
    filterset_fields = ['id', 'creator', 'likes']
    template_name = 'short-filter.html'




def saved_post_list(request):
    posts = Post.objects.filter(saved_posts__user=request.user)
    context = {'posts': posts}
    return render(request, 'saved_post_list.html', context)

def  update_post(request, id):
    context = {}
    post_object = Post.objects.get(id=id)
    if request.user != post_object.creator:
        return HttpResponse ('No access')
    if request.method == 'POST':
        post_form = PostForm(
            data=request.POST,
            files=request.FILES,
            instance=post_object
        )
        if post_form.is_valid():
            post_form.save()
            return redirect(post_detail, id=post_object.id)
        else:
            messages.warning(request, 'Form is not valid')
            return render(request, 'update_post.html', context)
    post_form = PostForm(instance=post_object)
    context['post_form'] = post_form
    return render(request, 'update_post.html', context)

def delete_post(request, id):
    post = Post.objects.get(id=id)
    if request.user != post.creator:
        return HttpResponse ('No access')
    post.delete()
    return redirect(homepage)


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

def update_short(request, id):
    short = Short.objects.get(id=id)
    if request.method == "POST":
        new_description = request.POST['description']
        short.description = new_description
        short.save()
        return redirect('short-info-cvb', id=short.id)
    context = {'short': short}
    return render(request, 'update_short.html', context)


class Short_listView(View):
    def get(self, request):
        short_filter = ShortFilter(
            request.GET,
            queryset=Short.objects.all()
        )
        short_lst = Short.objects.all()
        context = {'short_lst': short_lst}
        return render(request, 'short-lst-cvb.html', context, {'short_filter': short_filter})

class Short_videoView(DetailView):
    queryset = Short.objects.all()
    template_name = 'short_info-cvb.html'
    def get(self, request, *args, **kwargs):

        short_video = self.get_object()
        short_video.views_qty += 1
        if request.user.is_authenticated:
            short_video.viewed_users.add(request.user)
        short_video.save()
        return super().get(request, *args, **kwargs)

class ShortsFilterView(FilterView):
    model = Short
    filterset_class = ShortFilters
    filterset_fields = ['id', 'creator', 'views_qty']
    template_name = 'short-filter.html'




def short_video(request, id):
    short_video = Short.objects.get(id=id)
    short_video.views_qty += 1
    if request.user.is_authenticated:
        short_video.viewed_users.add(request.user)
    short_video.save()
    return render(request, 'short_video.html', {'short': short_video})


def short_list(request):
    short_filter = ShortFilter(
        request.GET,
        queryset=Short.objects.all()
    )
    short_lst = Short.objects.all()
    return render(request, 'short_lst.html', {'short_lst': short_lst}, {'short_filter': short_filter} )


def show_notification(request):
    note_lst = Notification.objects.filter(user=request.user)
    for note in note_lst:
        note.is_showed =True
        note_lst.bulk_update(note_lst, ['is_showed'])
    return render(request, 'note_lst.html', {'note_lst': note_lst})

class Show_notificationView(View):
    def get_note(self, request):
        note_lst = Notification.objects.filter(user=request.user)
        for note in note_lst:
            note.is_showed = True
            note_lst.bulk_update(note_lst, ['is_showed'])
        return render(request, 'note_lst.html', {'note_lst': note_lst})



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

def add_post_form(request):
    if request.method == "POST":
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post_object = post_form.save(commit=False)
            post_object.creator = request.user
            post_object.save()
            return redirect(post_detail, id=post_object.id)
        else:
            messages.warning(request, 'Form is not valid')


    post_form = PostForm()
    context = {}
    context['post_form'] = post_form
    return render(request, 'create_post_dj_form.html', context)


# def search(request):
#     return render(request, 'search.html')

class SearchView(View):
    def get(self, request):
        return render(request, 'search.html')


class Search_resultView(View):
    def get(self, request):
        key_word = request.GET['key_word']
        # posts = Post.objects.filter(name__icontains=key_word)
        posts = Post.objects.filter(
            Q(name__icontains=key_word) |
            Q(description__icontains=key_word)
        )
        context = {'posts': posts}
        return render(request, 'home.html', context)

# def search_result(request):
#     key_word = request.GET['key_word']
#     # posts = Post.objects.filter(name__icontains=key_word)
#     posts = Post.objects.filter(
#         Q(name__icontains=key_word) |
#         Q(description__icontains=key_word)
#     )
#     context = {'posts': posts}
#     return render(request, 'home.html', context)

def contacts(request):
    return redirect('contactus')


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
