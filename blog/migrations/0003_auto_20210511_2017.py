# Generated by Django 2.2.3 on 2021-05-11 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20210510_1925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='avatar',
            field=models.URLField(blank=True, max_length=400, verbose_name='标题图'),
        ),
    ]