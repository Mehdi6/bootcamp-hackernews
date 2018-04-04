from django.views.generic import CreateView, View, TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from services.forms import CommentForm
from .models import Topic, Comment, UpVoteTopic, UpVoteComment
from django.core.exceptions import ValidationError
from django.shortcuts import HttpResponse, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages

import logging

logger = logging.getLogger(__name__)


# Simple Topic view to create/add a topic by a user
@method_decorator(login_required, name='dispatch')
class TopicCreateView(CreateView):
    model = Topic
    fields = ['title', 'text', 'url']

    def form_valid(self, form):
        # This method is called when valid form data has been posted
        # Add the user who added the topic to the instance
        form.instance.user = self.request.user

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['navbar'] = 'add_topic'
        return ctx


class TopicDetailView(TemplateView):
    template_name = 'services/topic_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        topics = Topic.objects.filter(id=self.kwargs['id'])
        if len(topics) == 0:
            raise ValidationError('The given topic id is not valid.')

        topic = topics[0]
        comments = Comment.objects.filter(topic=topic)

        user = self.request.user
        if user.username != '':
            ups = UpVoteTopic.objects.filter(user=user, topic=topic)
            # If a user has upvoted the topic before, we add a variable
            # upvoted in order to hide he upvote carot on the template
            if len(ups) != 0:
                topic.up_voted = True

            for cmt in comments:
                cmt.up_voted = False
                ups = UpVoteComment.objects.filter(user=user, comment=cmt)
                # If a user has upvoted the topic before, we add a variable
                # upvoted in order to hide he upvote carot on the template
                if len(ups) != 0:
                    cmt.up_voted = True

        context['topic'] = topic
        context['comments'] = comments
        context['navbar'] = 'home'

        return context


@method_decorator(login_required, name='dispatch')
class CommentCreateView(View):
    template_name = "services/topic_detail.html"
    form_class = CommentForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        user = self.request.user
        topic = kwargs['id']

        # Validation of comment data
        additional_errors = []
        if form.is_valid():
            logger.info("Form is valid!")

            content = form.cleaned_data.get("comment_content")
            media = form.cleaned_data.get("comment_media")
            parent = form.cleaned_data.get("comment_parent")

            # validate topic id
            topics = Topic.objects.filter(id=topic)
            if len(topics) == 0:
                additional_errors.append("Topic id does not exists")
            else:
                tpc = topics[0]

            if parent:
                parent = Comment.objects.filter(id=parent)
                if len(parent) == 0:
                    additional_errors.append("Parent comment id does not exists!")
                    parent = None
                else:
                    parent = parent[0]

            if len(additional_errors) == 0:
                new_comment = Comment(content=content, media=media, topic=tpc, user=user, parent=parent)
                new_comment.save()

        else:
            msg_errors = form.errors.values()
            msg_errors = "\n".join([str(msg) for msg in msg_errors] + additional_errors)
            messages.add_message(request, messages.WARNING, msg_errors)

            logger.info(msg_errors)
            return redirect(
                reverse('services:topic_detail', args=[topic])
            )

        success_msg = "Comment added successfully"
        messages.add_message(request, messages.SUCCESS, success_msg)
        return redirect(
            reverse('services:topic_detail', args=[topic])
        )


@login_required
def upvote_topic(request):
    # validating the id first:
    id = request.POST['id']
    try:
        id = int(id)
    except ValueError:
        return HttpResponse(status=400)

    topics = Topic.objects.filter(id=id)
    # Message to return in case of an error, or when success
    # return 's' when success, return 'e' when error
    if len(topics) == 0:
        # flag error
        return HttpResponse(status=400)

    topic = topics[0]
    user = request.user

    # we check if the user has already upvoted the topic
    ups = UpVoteTopic.objects.filter(topic=topic, user=user)
    if len(ups) != 0:
        return HttpResponse(status=400)
    else:
        up_vote = UpVoteTopic(topic=topic, user=user)
        up_vote.save()

    return HttpResponse(status=200)


@login_required
def upvote_comment(request):
    id = request.POST['id']
    # Message to return in case of an error, or when success
    # return 's' when success, return 'e' when error
    msg = 's'
    try:
        id = int(id)
    except ValueError:
        return HttpResponse(status=400)
    # validating the id first:
    comments = Comment.objects.filter(id=id)

    if len(comments) == 0:
        # flag error
        return HttpResponse(status=400)

    comment = comments[0]
    user = request.user

    # we check if the user has already upvoted the topic
    ups = UpVoteComment.objects.filter(comment=comment, user=user)
    if len(ups) != 0:
        return HttpResponse(status=400)
    else:
        up_vote = UpVoteComment(comment=comment, user=user)
        up_vote.save()

    return HttpResponse(status=200)
