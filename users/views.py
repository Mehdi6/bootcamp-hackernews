from allauth.account.utils import send_email_confirmation
from django.views.generic import FormView, DetailView
from django.contrib.auth import authenticate, login
from django.contrib.messages.views import SuccessMessageMixin

from .forms import RegisterForm
from .models import User

import logging
logger = logging.getLogger(__name__)


class RegisterView(SuccessMessageMixin, FormView):
    template_name = 'account/signup.html'
    form_class = RegisterForm
    success_message = "One-Time password sent to your registered mobile number.\
                        The verification code is valid for 10 minutes."
    success_url = '/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        user = form.save()
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        logger.info("New user account registered {}".format(username))
        user = authenticate(username=username, password=password)
        login(self.request, user)

        send_email_confirmation(self.request, user)

        return super().form_valid(form)


class UserDetailView(DetailView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'profile'

        return context