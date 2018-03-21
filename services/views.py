from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import TemplateView, FormView
from django.views.generic import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
import json
from .forms import *
from .models import Topic, Comment

class FirstView(View):
    pass