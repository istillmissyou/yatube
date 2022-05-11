from django.conf import settings
from django.core.paginator import Paginator


def page_paginator(request, posts):
    paginator = Paginator(posts, settings.COUNTOBJ)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
