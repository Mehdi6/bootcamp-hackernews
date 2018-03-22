from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import logout
from .views import TopicCreateView, TopicListView

urlpatterns = [
    #url(r'^$', IndexView.as_view(), name="register_url"),
    #url(r'^login/', LoginView.as_view(), name="login_url"),
    # url(r'^verify/$', PhoneVerificationView.as_view(), name="phone_verification_url"),
    #url(r'^dashboard/$', DashboardView.as_view(), name="dashboard_url"),
    # url(r'^logout/$', logout, {'next_page': '/'})
    url(r'^topic/add/$', TopicCreateView.as_view(), name="create_topic"),
    url(r'^topic/list/$', TopicListView.as_view(), name="list_topic")
]
