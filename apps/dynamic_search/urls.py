from django.conf.urls import *
                           

urlpatterns = patterns('dynamic_search.views',
    url(r'^search/$', 'search', (), 'search'),
)
    

