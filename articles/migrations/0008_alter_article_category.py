# Generated by Django 3.2.7 on 2021-10-25 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0007_auto_20211025_0925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.CharField(choices=[('TC', 'Tecnologia'), ('SP', 'Sport'), ('SL', 'Salute'), ('AN', 'Anime'), ('TL', 'Tempo Libero')], default='TL', max_length=2),
        ),
    ]
