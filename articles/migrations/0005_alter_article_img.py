# Generated by Django 3.2.7 on 2021-10-09 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0004_alter_article_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='media/'),
        ),
    ]
