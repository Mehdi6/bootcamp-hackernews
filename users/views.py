from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import TemplateView, FormView, DetailView
from django.contrib.auth import authenticate, login
from django.contrib.messages.views import SuccessMessageMixin

from django.contrib import messages
import json
from .forms import RegisterForm
from .models import User

class RegisterView(SuccessMessageMixin, FormView):
    template_name = 'index.html'
    form_class = RegisterForm
    success_message = "One-Time password sent to your registered mobile number.\
                        The verification code is valid for 10 minutes."
    success_url = '/verify'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        user = form.save()
        #print(self.request.POST['username'])
        username = self.request.POST['username']
        password = self.request.POST['password1']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        response = send_verfication_code(user)
        data = json.loads(response.text)

        if data['success'] == False:
            messages.add_message(self.request, messages.ERROR,
                            data['message'])
            return redirect('/dashboard')

        #print(response.status_code, response.reason)
        #print(response.text)
        return super().form_valid(form)

class UserDetailView(DetailView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'

