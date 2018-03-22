from django.views.generic import CreateView, ListView, View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Topic

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


class TopicDetailView(View):
    
    pass

@method_decorator(login_required, name='dispatch')
class TopicUpvoteView(View):
    pass

@method_decorator(login_required, name='dispatch')
class CommentCreateView(View):
    pass

@method_decorator(login_required, name='dispatch')
class CommentUpvoteView(View):
    pass