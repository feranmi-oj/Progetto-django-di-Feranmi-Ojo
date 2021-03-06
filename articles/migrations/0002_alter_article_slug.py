# Generated by Django 3.2.7 on 2021-10-06 08:13

from django.db import migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(blank=True, editable=False, max_length=250, populate_from=('title',), unique=True, verbose_name='slug'),
        ),
    ]
