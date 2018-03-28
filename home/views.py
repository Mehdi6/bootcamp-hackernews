from django.views.generic import TemplateView
from services.models import Topic, UpVoteTopic


class IndexView(TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        topics = Topic.objects.all().order_by("created_at")

        user = self.request.user
        #print(user)
        if user.username != '':
            for tpc in topics:
                ups = UpVoteTopic.objects.filter(user= user, topic=tpc)
                # If a user has upvoted the topic before, we add a variable
                # upvoted in order to hide he upvote carot on the template
                if len(ups) != 0:
                    tpc.up_voted = True

        context['topic_list'] = topics

        return context

class AboutView(TemplateView):
    template_name = 'home/about.html'

