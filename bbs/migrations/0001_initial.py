# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-17 19:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('objects', '0009_remove_objectdb_db_player'),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('db_key', models.CharField(db_index=True, max_length=35)),
                ('db_timeout', models.IntegerField(null=True)),
                ('lock_storage', models.TextField(null=True)),
                ('db_description', models.TextField()),
                ('db_members', models.ManyToManyField(to='objects.ObjectDB')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('db_author', models.CharField(max_length=50)),
                ('db_message', models.TextField()),
                ('db_likes', models.IntegerField()),
                ('db_date_posted', models.DateField()),
                ('db_has_liked', models.ManyToManyField(null=True, to='objects.ObjectDB')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('db_key', models.CharField(db_index=True, max_length=35)),
                ('db_message', models.TextField()),
                ('db_sender', models.CharField(max_length=50)),
                ('db_likes', models.IntegerField()),
                ('db_date_posted', models.DateField()),
                ('db_comments', models.ManyToManyField(null=True, to='bbs.Comment')),
                ('db_has_liked', models.ManyToManyField(null=True, to='objects.ObjectDB')),
                ('db_has_read', models.ManyToManyField(null=True, to='objects.ObjectDB')),
            ],
        ),
        migrations.AddField(
            model_name='board',
            name='db_posts',
            field=models.ManyToManyField(to='bbs.Post'),
        ),
    ]
