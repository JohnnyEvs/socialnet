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
    photo = models.ImageField('Photo', null=True, blank=True)
    status = models.CharField('Status',max_length=200, choices=STATUS_CHOICES)

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
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, null=True)

    def __str__(self):
        return f'{self.name} - {self.rating}'

class Meta():
    verbose_name = 'Post'
    verbose_name_plural = 'Posts'



