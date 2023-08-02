from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length = 55)
    description = models.TextField(null=True, blank=True)

class Post(models.Model):
    STATUS_CHOICES = (
        ('Posted', 'Posted'),
        ('Unposted', 'Unposted')
    )

    name = models.CharField('Header',max_length=80)
    description = models.TextField('Description', null=True)
    photo = models.ImageField('Photo', null=True, blank=True, upload_to='post_images/')
    status = models.CharField('Status',max_length=200, choices=STATUS_CHOICES, default="Posted")
    creator=models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        verbose_name="Post author",
        related_name='Posts'
    )
    category = models.ManyToManyField(
        to='Category', blank=True, verbose_name='Categories',
    )
    likes = models.PositiveIntegerField('Likes', default=0)

    def __str__(self):
        return f'{self.name} - {self.status}'

class Category(models.Model):
    RATING_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10)
    )

    name = models.CharField(max_length=50)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, null=True, blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    def __str__(self):
        return f'{self.name} - {self.rating}'


class Comment(models.Model):
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
    )
    comment_text = models.TextField()
    likes_qty = models.IntegerField (default=0)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['created_at']

    def __str__(self):
        return self.comment_text[:20]

class Short(models.Model):
    user = models.ForeignKey(User, verbose_name='Posted by', on_delete=models.CASCADE)
    video = models.FileField('Video', null=True, blank=True, upload_to='post_videos/')
    created_at = models.DateTimeField('Upload data', auto_now_add=True)
    views_qty = models.PositiveIntegerField('Views', default=0)

    class Meta:
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'

    def __str__(self):
        return f'{self.video} - {self.created_at}'


class SavedPosts(models.Model):
    user = models.OneToOneField(User, verbose_name='User', on_delete=models.CASCADE)
    post = models.ManyToManyField(Post,
                                  verbose_name='Saved post',
                                  related_name='saved_posts')

    class Meta:
        verbose_name = 'Saved Post'
        verbose_name_plural = 'Saved Posts'

    def __str__(self):
        return f'{self.user} - {self.post}'

