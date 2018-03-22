# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-03-21 16:22
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=2000, verbose_name='content')),
                ('created_at', models.DateField(auto_now=True, verbose_name='created_at')),
                ('comment_parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='child_comment', to='services.Comment', verbose_name='Comment')),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('url', models.URLField(blank=True, null=True)),
                ('text', models.CharField(max_length=200, verbose_name='text')),
                ('creation_at', models.DateField(auto_now=True, verbose_name='created_at')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topic', to=settings.AUTH_USER_MODEL, verbose_name='The topic')),
            ],
        ),
        migrations.CreateModel(
            name='UpVoteComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now=True, verbose_name='created_at')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='upvotes_comment', to='services.Comment', verbose_name='Upvoted Comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_up_voted', to=settings.AUTH_USER_MODEL, verbose_name='Upvoted comments')),
            ],
        ),
        migrations.CreateModel(
            name='UpVoteTopic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now=True, verbose_name='created_at')),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='upvotes_topic', to='services.Topic', verbose_name='Upvoted Topics')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topic_up_voted', to=settings.AUTH_USER_MODEL, verbose_name='Upvoted topics')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topic', to='services.Topic', verbose_name='Topic'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
    ]