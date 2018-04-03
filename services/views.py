import urllib

from django.views.generic import CreateView, ListView, View, TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from services.forms import CommentForm
from .models import Topic, Comment, UpVoteTopic, UpVoteComment
from django.core.exceptions import ValidationError
from django.shortcuts import HttpResponse, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages

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


class TopicDetailView(TemplateView):
    template_name = 'services/topic_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        topics = Topic.objects.filter(id = self.kwargs['id'])
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
                cmt.subcomment_count = cmt.get_descendant_count()
                ups = UpVoteComment.objects.filter(user= user, comment=cmt)
                # If a user has upvoted the topic before, we add a variable
                # upvoted in order to hide he upvote carot on the template
                if len(ups) != 0:
                    cmt.up_voted = True

        context['topic'] = topic
        context['comments'] = comments
        msg = self.request.GET.get("message")
        tag = self.request.GET.get("tag")

        if msg and tag:
            if tag == 's':
                messages.success(self.request, msg)
            elif tag == 'w':
                messages.warning(self.request, msg)

        return context

@login_required
def upvote_topic(request, id):
    # validating the id first:
    topics = Topic.objects.filter(id=id)
    msg = 's'
    if len(topics) == 0:
        # flag error
        msg = 'e'
    
    topic = topics[0]
    user = request.user
    
    # we check if the user has already upvoted the topic
    ups = UpVoteTopic.objects.filter(topic=topic, user=user)
    if len(ups) != 0:
        msg = 'e'
    else:
        up_vote = UpVoteTopic(topic=topic, user=user)
        up_vote.save()
        # we increment the number of up_votes on the topic
        topic.up_votes += 1
        topic.save()
    return HttpResponse(msg)


@login_required
def upvote_comment(request, id):
    # validating the id first:
    comments = Comment.objects.filter(id=id)
    msg = 's'
    if len(comments) == 0:
        # flag error
        msg = 'e'

    comment = comments[0]
    user = request.user

    # we check if the user has already upvoted the topic
    ups = UpVoteComment.objects.filter(comment=comment, user=user)
    if len(ups) != 0:
        msg = 'e'
    else:
        up_vote = UpVoteComment(comment=comment, user=user)
        up_vote.save()
        # we increment the number of up_votes on the topic
        comment.up_votes += 1
        comment.save()

    return HttpResponse(msg)

@method_decorator(login_required, name='dispatch')
class CommentCreateView(View):
    template_name = "services/topic_detail.html"
    form_class = CommentForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        user = self.request.user
        topic = kwargs['id']
        content = request.POST.get("comment_content")
        media = request.POST.get("comment_media")
        parent = request.POST.get("comment_parent")

        # Validation of comment data
        additional_errors = []
        if form.is_valid():
            #print("Form is valid!")
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
                #print(new_comment)
                #print(tpc)
                # new comment added
                tpc.comment_count +=1
                tpc.save()

        else:
            msg_errors = form.errors.values()
            msg_errors = "\n".join([str(msg) for msg in msg_errors] + additional_errors)

            ##print(msg_errors)
            return redirect("{}?{}".format(
                    reverse('services:topic_detail', args=[topic]),
                    urllib.parse.urlencode(
                        {'message': msg_errors, 'tag':'w'})
                        ))

        success_msg = "Comment added successfully"
        return redirect("{}?{}".format(
                    reverse('services:topic_detail', args=[topic]),
                    urllib.parse.urlencode({'message':success_msg, 'tag':'s'})
                        ))

