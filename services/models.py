from django.db import models
from django.utils.translation import ugettext_lazy as _

from users.models import User
from mptt.models import MPTTModel, TreeForeignKey


class Topic(models.Model):
    title = models.CharField(_('Title'), max_length=200, blank=False, null=False)
    url = models.URLField(_('URL'), blank=False, null=False)
    text = models.TextField(_('Text'), max_length=500, blank=False, null=False)
    created_at = models.DateTimeField(_("created_at"), auto_now=True)

    user = models.ForeignKey(User, related_name="topic",
                             verbose_name="User", on_delete=models.CASCADE)

    @property
    def up_votes(self):
        return UpVoteTopic.objects.filter(topic=self).count()

    @property
    def comment_count(self):
        return self.comments.count()

    def __str__(self):
        return "ID={} Title={} url={} text={} comment_count={}".format(
            self.id, self.title, self.url, self.text, self.comment_count)


class Comment(MPTTModel):
    class MPTTMeta:
        order_insertion_by = ['created_at']

    content = models.TextField(_('content'), max_length=2000, blank=False, null=False)
    parent = TreeForeignKey('self', related_name="child_comment",
                            verbose_name="Comment", blank=True, db_index=True, null=True)
    media = models.URLField(blank=True, null=True)
    user = models.ForeignKey(User, related_name="comment",
                             verbose_name="user", on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, related_name="comments",
                              verbose_name="Topic", on_delete=models.CASCADE)

    @property
    def up_votes(self):
        return self.upvotes_comment.count()
    
    @property
    def subcomment_count(self):
        return self.get_descendant_count()

    created_at = models.DateField(_("created_at"), auto_now=True)

    def __str__(self):
        return "ID={} Content={} user={} topic={} subcomments_count={}".format(self.id, self.content, self.user,
                                                                               self.topic, self.get_descendant_count())


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
