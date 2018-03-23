from django.conf.urls import url
from .views import (TopicCreateView, TopicDetailView, TopicUpvoteView,
                    CommentUpvoteView, CommentCreateView, upvote_topic)

urlpatterns = [
    url(
        regex=r'^topic/add/$',
        view=TopicCreateView.as_view(),
        name="create_topic"
        ),
    url(
        regex=r'^topic/upvote/(?P<id>\d+)/$',
        view=upvote_topic,
        name="topic_upvote"
        ),
    url(
        regex=r'^topic/(?P<id>\d+)/$',
        view=TopicDetailView.as_view(),
        name="topic_detail"
        ),
    url(
        regex=r'^comment/add/(?P<id>\d+)/$',
        view=CommentCreateView.as_view(),
        name="create_comment"
        ),
    url(
        regex=r'^comment/upvote/(?P<id>\d+)/$',
        view=CommentUpvoteView.as_view(),
        name="comment_upvote"
        ),
]
