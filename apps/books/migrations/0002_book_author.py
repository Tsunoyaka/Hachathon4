# Generated by Django 4.1.3 on 2022-11-10 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='author',
            field=models.CharField(default=1, max_length=100, verbose_name='Автор'),
            preserve_default=False,
        ),
    ]
