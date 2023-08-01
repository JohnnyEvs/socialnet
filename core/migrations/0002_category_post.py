# Generated by Django 4.2.3 on 2023-08-01 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('rating', models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)])),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, verbose_name='Header')),
                ('description', models.TextField(null=True, verbose_name='Description')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Photo')),
                ('status', models.CharField(choices=[('Posted', 'Posted'), ('Unposted', 'Unposted')], max_length=200, verbose_name='Status')),
            ],
        ),
    ]
