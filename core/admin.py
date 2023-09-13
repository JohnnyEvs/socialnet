from django.contrib import admin
from .models import Profile, Post, Category, Comment, Short, SavedPosts, Notification

# Register your models here.
class CommentInLine(admin.TabularInline):
    model = Comment
    extra = 0

admin.site.register(Profile)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['name', 'likes', 'creator', 'status']
    list_filter = ['status', 'creator']
    search_fields = ['name', 'description',
                     'status', 'creator_username', 'creator_first_name']
    inlines = [CommentInLine]
    list_editable = ['status']

@admin.register(SavedPosts)
class SavedPosts(admin.ModelAdmin):
    list_display = ['user']
    search_fields = ['user']


@admin.register(Short)
class ShortAdmin(admin.ModelAdmin):
    list_display = ['video', 'user', 'views_qty']
    list_filter = ['user', 'views_qty']
    search_fields = ['user', 'video']




admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Notification)

