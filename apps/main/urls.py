from django.conf.urls import *


urlpatterns = patterns('main.views',
    url(r'^$', 'home', (), 'home'),
)
