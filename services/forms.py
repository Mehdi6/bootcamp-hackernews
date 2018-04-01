from django import forms
from django.utils.translation import ugettext as _

from .models import Topic, Comment

import logging
logger = logging.getLogger(__name__)


class TopicForm(forms.ModelForm):
    title = forms.CharField(required=True)
    url = forms.URLField(required=True)
    text = forms.CharField(min_length=50, widget=forms.Textarea, required=False)

    class Meta:
        model = Topic
        fields = ['title', 'url', 'text']

    def clean_title(self):
        # add some contraints to validate the title
        title = self.data.get('title')
        return title

    def save(self, *args, **kwargs):
        topic = super(TopicForm, self).save(*args, **kwargs)
        logger.info('Saving topic')
        return topic


class CommentForm(forms.ModelForm):
    comment_content = forms.CharField(max_length=2000, widget=forms.Textarea, required=True)
    comment_media = forms.URLField(required=False)
    comment_parent = forms.IntegerField(required=False)  # Validation for positif numbers

    class Meta:
        model = Comment
        fields = []#['content', 'media', 'parent']

    def clean_comment_content(self):
        # add some constraints to validate the title
        content = self.data.get('comment_content')
        return content


