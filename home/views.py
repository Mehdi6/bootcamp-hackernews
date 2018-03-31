from django.views.generic import TemplateView
from services.models import Topic, UpVoteTopic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, Page

import logging

logger = logging.getLogger(__name__)


def extend_pagination(page, size_extension):
    remain_left = False
    remain_right = False
    range_extension = []

    len_paginator = page.paginator.num_pages
    current_page = page.number

    step_right = max(0, min(len_paginator - current_page, size_extension))
    step_left = min(size_extension * 2 - step_right, current_page - 1)
    step_right += min(len_paginator - current_page - step_right, max(0, size_extension - step_left))

    if step_right == 0 and step_left == 0:
        return {'remain_left': remain_left, 'remain_right': remain_right, 'ex_range': range_extension}

    if len_paginator - current_page > step_right:
        remain_right = True

    if current_page - size_extension > 1:
        remain_left = True

    for i in range(step_left):
        range_extension.insert(0, current_page - i - 1)

    range_extension.append(current_page)

    for i in range(step_right):
        range_extension.append(current_page + i + 1)

    return {'remain_left': remain_left, 'remain_right': remain_right, 'ex_range': range_extension}


class IndexView(TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        page = self.request.GET.get("page");
        context = super().get_context_data(**kwargs)
        topics = Topic.objects.all()

        sort_by = self.request.GET.get("sortBy")
        if sort_by == 'recent':
            topics = topics.order_by('created_at')
            context["sort_by"] = 'recent'
            logger.info('recent')
        elif sort_by == 'rate':
            context['sort_by'] = 'rate'
            topics = sorted(topics, key=lambda x: x.up_votes, reverse=True)
            logger.info('rated')
            
        user = self.request.user
        logger.info(user)
        if user.username != '':
            for tpc in topics:
                ups = UpVoteTopic.objects.filter(user=user, topic=tpc)
                # If a user has upvoted the topic before, we add a variable
                # upvoted in order to hide he upvote carot on the template
                if len(ups) != 0:
                    tpc.up_voted = True

        context['page'] = (page, 1)[page == None]

        # pagination at last
        pagination = Paginator(topics, 10)

        try:
            context['pagination'] = pagination.page(context['page'])
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            context['pagination'] = pagination.page(1)
            context['page'] = 1
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            context['pagination'] = pagination.page(pagination.num_pages)
            context['page'] = pagination.num_pages

        context['pagination_ext'] = extend_pagination(context['pagination'], 2)
        context['navbar'] = 'home'

        return context


class AboutView(TemplateView):
    template_name = 'home/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'about'

        return context
