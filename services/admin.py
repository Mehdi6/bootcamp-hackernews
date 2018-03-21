from django.contrib import admin
from .models import Topic, Comment
# Register your models here.
# from django.contrib.auth.admin import UserAdmin
#
admin.site.register(Topic)
admin.site.register(Comment)
