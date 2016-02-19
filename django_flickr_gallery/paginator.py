from __future__ import unicode_literals
from django.core.paginator import PageNotAnInteger, EmptyPage
from django.utils import six


class Page(object):
    def __init__(self, object_list, number, paginator):
        self.object_list = object_list
        self.number = number
        self.paginator = paginator

    def __repr__(self):
        return '<Page %s of %s>' % (self.number, self.paginator.num_pages)

    def __len__(self):
        return len(self.object_list)

    def __getitem__(self, index):
        if not isinstance(index, (slice,) + six.integer_types):
            raise TypeError
        # The object_list is converted to a list so that if it was a QuerySet
        # it won't be a database hit per __getitem__.
        if not isinstance(self.object_list, list):
            self.object_list = list(self.object_list)
        return self.object_list[index]

    def __iter__(self):
        for photo in self.object_list:
            yield photo

    def has_next(self):
        return self.number < self.paginator.num_pages

    def has_previous(self):
        return self.number > 1

    def has_other_pages(self):
        return self.has_previous() or self.has_next()

    def next_page_number(self):
        return self.paginator.validate_number(self.number + 1)

    def previous_page_number(self):
        return self.paginator.validate_number(self.number - 1)

    def start_index(self):
        """
        Returns the 1-based index of the first object on this page,
        relative to total objects in the paginator.
        """
        # Special case, return zero if no items.
        if self.paginator.count == 0:
            return 0
        return (self.paginator.per_page * (self.number - 1)) + 1

    def end_index(self):
        """
        Returns the 1-based index of the last object on this page,
        relative to total objects found (hits).
        """
        # Special case for the last page because there can be orphans.
        if self.number == self.paginator.num_pages:
            return self.paginator.count
        return self.number * self.paginator.per_page


class Paginator(object):
    def __init__(self, iterator, per_page=10, page=None, pages=None, total=None):
        self.data = iterator
        self.per_page = per_page
        self.num_pages = pages or 1
        self.total = total or 1
        self.current_page_number = int(page or 1)
        self.page = Page(self.data, self.current_page_number, self)

    def __repr__(self):
        return "<Paginator />"

    def _page_range(self):
        return range(1, self.num_pages + 1)
    page_range = property(_page_range)

    def validate_number(self, number):
        """
        Validates the given 1-based page number.
        """
        try:
            number = int(number)
        except (TypeError, ValueError):
            raise PageNotAnInteger('That page number is not an integer')
        if number < 1:
            raise EmptyPage('That page number is less than 1')
        if number > self.num_pages:
            if number == 1 and self.allow_empty_first_page:
                pass
            else:
                raise EmptyPage('That page contains no results')
        return number

    def _first_page(self):
        return 1
    first_page = property(_first_page)

    def _last_page(self):
        return self.num_pages
    last_page = property(_last_page)


def get_paginator(iterator, page=None, per_page=10, pages=None, total=None):
    paginator = Paginator(
        iterator, per_page=per_page,
        page=page, pages=pages,
        total=total)

    page = paginator.page

    return paginator, page