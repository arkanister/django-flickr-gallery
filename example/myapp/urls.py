from django.conf.urls import patterns, url

urlpatterns = patterns('example.myapp.views',
    url('^$', 'get_featured_photosets', name='get_featured_photosets'),
)
