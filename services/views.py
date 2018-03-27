import urllib

from django.views.generic import CreateView, ListView, View, TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from services.forms import CommentForm
from .models import Topic, Comment
from django.core.exceptions import ValidationError
from django.shortcuts import HttpResponse, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages

# Simple Topic view to create/add a topic by a user
@method_decorator(login_required, name='dispatch')
class TopicCreateView(CreateView):
    #template_name = 'services/topic_form.html'
    #form_class = TopicForm
    #success_url = 'topic_added.html'
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
        comments = Comment.objects.filter(topic=topic)#.order_by("-created_at")
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

@method_decorator(login_required, name='dispatch')
class TopicUpvoteView(View):
    pass

@login_required
def upvote_topic(request):
    print(request['id'])
    return HttpResponse('Hello my dear!')

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
            print("Form is valid!")
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
                print(new_comment)
                print(tpc)
                # new comment added
                tpc.comment_count +=1
                tpc.save()

        else:
            msg_errors = form.errors.values()
            msg_errors = "\n".join([str(msg) for msg in msg_errors] + additional_errors)

            #print(msg_errors)
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

@method_decorator(login_required, name='dispatch')
class CommentUpvoteView(View):
    pass