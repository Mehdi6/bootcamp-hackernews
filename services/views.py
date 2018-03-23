from django.views.generic import CreateView, ListView, View, TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Topic, Comment
from django.core.exceptions import ValidationError
from django.shortcuts import HttpResponse

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
        context['topic'] = topic
        context['comments'] = Comment.objects.filter(topic=topic).order_by('created_at')

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
    pass

@method_decorator(login_required, name='dispatch')
class CommentUpvoteView(View):
    pass