# Generated by Django 3.2.7 on 2021-10-26 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0008_alter_article_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.CharField(choices=[('TC', 'Technology'), ('SP', 'Sport'), ('HT', 'Health'), ('AN', 'Anime'), ('FT', 'Free time')], default='FT', max_length=2),
        ),
    ]
