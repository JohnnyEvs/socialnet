# Generated by Django 4.2.3 on 2023-08-17 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='dislikes',
            field=models.PositiveIntegerField(default=0, verbose_name='Dislikes'),
        ),
    ]