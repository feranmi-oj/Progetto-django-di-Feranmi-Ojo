# Generated by Django 3.2.7 on 2021-11-05 08:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0015_article_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='likes',
        ),
    ]