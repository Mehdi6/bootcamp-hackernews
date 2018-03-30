from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth.password_validation import validate_password

from .models import User

import logging
logger = logging.getLogger(__name__)


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    MIN_LENGTH = 4

    class Meta:
        model = User
        fields = ['username', 'email', 'password1',
                    'password2', 'full_name' ]

    def clean_username(self):
        username = self.data.get('username')
        return username

    def clean_password1(self):
        password = self.data.get('password1')
        validate_password(password)
        if password != self.data.get('password2'):
            raise forms.ValidationError(_("Passwords do not match"))
        return password

    def clean_email(self):
        # if email already exists, then send back validation error
        email = self.data.get('email')
        results = User.objects.filter(email=email)
        logger.info(results)
        if len(results) != 0:
            raise forms.ValidationError(_("Email address already exists"))

        return email

    def save(self, *args, **kwargs):
        user = super(RegisterForm, self).save(*args, **kwargs)
        user.set_password(self.cleaned_data['password1'])
        logger.info('Saving user with country_code', user.country_code)
        user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

    class Meta:
        fields = ['username','password']
