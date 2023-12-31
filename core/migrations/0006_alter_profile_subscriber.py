# Generated by Django 4.2.3 on 2023-08-15 04:26

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0005_alter_profile_subscriber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='subscriber',
            field=models.ManyToManyField(blank=True, related_name='followed_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
