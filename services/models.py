from django.db import models
from django.utils.translation import ugettext_lazy as _

from users.models import User


class Topic(models.Model):
    title = models.CharField(_('title'), max_length=200, blank=False, null=False)
    url = models.URLField(blank=False, null=False)
    text = models.CharField(_('text'), max_length=200, blank=False, null=False)
    created_at = models.DateField(_("created_at"), auto_now=True)

    user = models.ForeignKey(User, related_name="topic",
                                  verbose_name="User",on_delete=models.CASCADE)

    upvotes = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)

class Comment(models.Model):
    content = models.TextField(_('content'), max_length=2000, blank=False, null=False)

    comment_parent = models.ForeignKey('self', related_name="child_comment",
                                       verbose_name="Comment", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="comment",
                                       verbose_name="user", on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, related_name="topic",
                             verbose_name="Topic", on_delete=models.CASCADE)
    created_at = models.DateField(_("created_at"), auto_now=True)


class UpVoteComment(models.Model):
    created_at = models.DateField(_("created_at"), auto_now=True)
    comment = models.ForeignKey(Comment, related_name="upvotes_comment",
                                       verbose_name="Upvoted Comment", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="comment_up_voted",
                                       verbose_name="Upvoted comments", on_delete=models.CASCADE)


class UpVoteTopic(models.Model):
    created_at = models.DateField(_("created_at"), auto_now=True)
    topic = models.ForeignKey(Topic, related_name="upvotes_topic",
                                verbose_name="Upvoted Topics", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="topic_up_voted",
                             verbose_name="Upvoted topics", on_delete=models.CASCADE)
