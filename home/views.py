from django.views.generic import TemplateView
from services.models import Topic

class IndexView(TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topic_list'] = Topic.objects.all()

        return context

class AboutView(TemplateView):
    template_name = 'home/about.html'

