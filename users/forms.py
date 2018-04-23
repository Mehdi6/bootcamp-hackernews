from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.contrib.auth.password_validation import validate_password

from .models import User

import logging

logger = logging.getLogger(__name__)


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput())
    password2 = forms.CharField(label=_('Password (again)'), widget=forms.PasswordInput())

    MIN_LENGTH = 4

    class Meta:
        model = User
        fields = ['username', 'email', 'password1',
                  'password2', 'full_name']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'full_name': forms.TextInput(attrs={'placeholder': 'Full name'}),
        }

    def validate_username(self, username):
        # we check if the username does exist
        print(username)
        results = User.objects.filter(username=username)
        if len(results) != 0:
            print("There is an error here!")
            raise forms.ValidationError(_("Username already exists"))
        return username

    def validate_password1(self, password):
        print(password)
        try:
            validate_password(password)
        except ValidationError:
            raise forms.ValidationError(_("Invalid password!"))

        if password != self.data.get('password2'):
            raise forms.ValidationError(_("Passwords do not match"))
        return password

    def validate_email(self, email):
        # if email already exists, then send back validation error
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
        fields = ['username', 'password']
