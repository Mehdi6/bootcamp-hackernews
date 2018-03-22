from django.conf.urls import url
from .views import TopicCreateView, TopicDetailView, TopicUpvoteView, CommentUpvoteView, CommentCreateView

urlpatterns = [
    url(r'^topic/add/$', TopicCreateView.as_view(), name="create_topic"),
    url(r'^topic/upvote/(?P<id>\d+)/$', TopicUpvoteView.as_view(), name="topic_upvote"),
    url(r'^topic/(?P<id>\d+)/$', TopicDetailView.as_view(), name="topic_detail"),
    url(r'^comment/add/(?P<id>\d+)/$', CommentCreateView.as_view(), name="create_comment"),
    url(r'^comment/upvote/(?P<id>\d+)/$', CommentUpvoteView.as_view(), name="comment_upvote"),
]
