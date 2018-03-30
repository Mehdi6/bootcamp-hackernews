from django import forms
from django.utils.translation import ugettext as _

from .models import Topic, Comment


import logging
logger = logging.getLogger(__name__)

class TopicForm(forms.ModelForm):
    title = forms.CharField(required=True)
    url = forms.URLField()
    text = forms.CharField(min_length=50, widget=forms.Textarea)

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
        #topic.save()
        return topic
