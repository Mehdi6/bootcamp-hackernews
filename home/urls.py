from django.conf.urls import url
from django.contrib import admin
from allauth.account.views import LoginView
from .views import IndexView, AboutView

urlpatterns = [
    url(
        regex=r'^$',
        view=IndexView.as_view(),
        name="home"
        ),
    url(regex=r'^about/',
        view=AboutView.as_view(),
        name="about"
        ),
    url(regex=r'^login$',
        view=LoginView.as_view(),
        name="login"
        )
]
