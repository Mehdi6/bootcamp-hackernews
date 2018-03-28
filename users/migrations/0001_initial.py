# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-03-21 16:22
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import users.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0007_alter_validators_add_error_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=130, unique=True, verbose_name='username')),
                ('full_name', models.CharField(blank=True, max_length=130, verbose_name='full name')),
                ('email', models.EmailField(blank=True, max_length=50, verbose_name='email id')),
                ('is_staff', models.BooleanField(default=False, verbose_name='is_staff')),
                ('is_active', models.BooleanField(default=True, verbose_name='is_active')),
                ('date_joined', models.DateField(default=datetime.date.today, verbose_name='date_joined')),
                ('phone_number_verified', models.BooleanField(default=False)),
                ('change_pw', models.BooleanField(default=True)),
                ('phone_number', models.BigIntegerField(blank=True, null=True)),
                ('country_code', models.IntegerField(blank=True, null=True)),
                ('profile_picture', models.URLField(blank=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'ordering': ('username',),
            },
            managers=[
                ('objects', users.manager.UserManager()),
            ],
        ),
    ]
