# Generated by Django 2.2.3 on 2021-05-10 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='avatar',
            field=models.URLField(blank=True, max_length=350, verbose_name='标题图'),
        ),
    ]