from django.conf.urls import url
from .views import UserDetailView

urlpatterns = [
    url(
        regex=r'^(?P<username>[\w.@+-]+)/$',
        view=UserDetailView.as_view(),
        name='detail'
        ),
]
