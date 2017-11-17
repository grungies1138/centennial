# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-17 19:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('objects', '0009_remove_objectdb_db_player'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bucket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('db_key', models.CharField(db_index=True, max_length=25)),
                ('db_description', models.TextField()),
                ('db_sla', models.IntegerField()),
                ('lock_storage', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('db_key', models.CharField(db_index=True, max_length=50)),
                ('db_status', models.CharField(choices=[(b'N', b'NEW'), (b'I', b'In Progress'), (b'H', b'ON HOLD'), (b'W', b'WAITING'), (b'C', b'CLOSED')], max_length=1)),
                ('db_completed_date', models.DateTimeField(null=True)),
                ('db_opened_date', models.DateTimeField()),
                ('lock_storage', models.TextField()),
                ('db_assigned_to', models.ManyToManyField(null=True, to='objects.ObjectDB')),
                ('db_bucket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.Bucket')),
            ],
        ),
        migrations.CreateModel(
            name='JobMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('db_date_sent', models.DateTimeField()),
                ('db_message', models.TextField()),
                ('db_job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.Job')),
                ('db_sender', models.ManyToManyField(to='objects.ObjectDB')),
            ],
        ),
        migrations.CreateModel(
            name='Roll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('db_skill', models.CharField(max_length=50)),
                ('db_roll', models.IntegerField()),
                ('db_job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.Job')),
                ('db_roller', models.ManyToManyField(to='objects.ObjectDB')),
            ],
        ),
        migrations.AddField(
            model_name='job',
            name='db_messages',
            field=models.ManyToManyField(to='jobs.JobMessage'),
        ),
        migrations.AddField(
            model_name='job',
            name='db_rolls',
            field=models.ManyToManyField(null=True, to='jobs.Roll'),
        ),
        migrations.AddField(
            model_name='job',
            name='db_viewers',
            field=models.ManyToManyField(to='objects.ObjectDB'),
        ),
        migrations.AddField(
            model_name='bucket',
            name='db_jobs',
            field=models.ManyToManyField(null=True, to='jobs.Job'),
        ),
    ]
