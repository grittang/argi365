# Generated by Django 2.2.3 on 2021-05-22 17:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20210523_0113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='channel',
            field=models.ForeignKey(default='insights', on_delete=django.db.models.deletion.CASCADE, to='blog.Channel', verbose_name='版块'),
        ),
        migrations.AlterField(
            model_name='channel',
            name='name',
            field=models.CharField(choices=[('insights', '洞察'), ('resources', '资源')], default='insights', max_length=20),
        ),
    ]
