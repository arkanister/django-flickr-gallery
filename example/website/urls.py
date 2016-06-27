from django.conf.urls import url

import example.website.views

urlpatterns = [
    url('^$', example.website.views.get_featured_photosets, name='get_featured_photosets'),
]
