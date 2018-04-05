from django.conf.urls import url

from .views import (TopicCreateView, TopicDetailView,
                    CommentCreateView, upvote_topic, upvote_comment)

urlpatterns = [
    url(
        regex=r'^topic/add/$',
        view=TopicCreateView.as_view(),
        name="create_topic",
        ),
    url(
        regex=r'^topic/upvote/$',
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
        regex=r'^comment/upvote/$',
        view=upvote_comment,
        name="comment_upvote"
        ),
]
