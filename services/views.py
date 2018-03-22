from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import CreateView, ListView
from django.views.generic import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
import json
from .forms import TopicForm
from .models import Topic, Comment

# Simple Topic view to create/add a topic by a user
@method_decorator(login_required, name='dispatch')
class TopicCreateView(CreateView):
    #template_name = 'services/topic_form.html'
    #form_class = TopicForm
    #success_url = 'topic_added.html'
    model = Topic
    fields = ['title', 'text', 'url']

    def form_valid(self, form):
        # This method is called when valid form data has been posted
        # Add the user who added the topic to the instance
        form.instance.user = self.request.user

        return super().form_valid(form)

# Simple Topic view to List created topics
class TopicListView(ListView):
    model = Topic

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    