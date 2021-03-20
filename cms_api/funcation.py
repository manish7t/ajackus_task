from django.db.models import Q
from .models import Content


def search_contant(**kwargs):
    search_keyword = kwargs['search_keyword']
    print(search_keyword)
    content_list = Content.objects.filter(Q(title__icontains=search_keyword) |
                                          Q(body__icontains=search_keyword) |
                                          Q(summary__icontains=search_keyword) |
                                          Q(categories__name__icontains=search_keyword))

    return content_list
