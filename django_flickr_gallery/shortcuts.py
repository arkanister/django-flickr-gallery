from django_flickr_gallery import settings


Paginator = getattr(settings, 'PAGINATOR_CLASS')


def get_paginator(iterator, page=None, per_page=10, pages=None, total=None):
    """
    Returns paginator instance from the iterator object.
    :param iterator:
        Iterator object to paginate.
    :param page:
        Number of current page. If not default 1.
    :param per_page:
        How many objects per page.
    :param pages:
        Total pages count.
    :param total:
        Total objects count.
    :return: paginator and page_obj
    """
    paginator = Paginator(
        iterator, per_page=per_page,
        page=page, pages=pages,
        total=total)
    return paginator, paginator.page
