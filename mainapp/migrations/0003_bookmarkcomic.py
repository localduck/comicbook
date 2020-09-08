# Generated by Django 3.0.8 on 2020-08-09 13:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainapp', '0002_auto_20200802_1816'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookmarkComic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_number', models.IntegerField()),
                ('comic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Comic', verbose_name='Comic')),
                ('comic_reader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Comic_Reader_User')),
            ],
            options={
                'db_table': 'bookmark_comic',
            },
        ),
    ]
