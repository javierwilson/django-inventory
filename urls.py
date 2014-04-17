from django.conf.urls import *
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    #----Django
    #(r'^orig_admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

    #(r'^i18n/', include('django.conf.urls.i18n')),

    #----Grappelli
    (r'^grappelli/', include('grappelli.urls')),
    
    #----Project
    (r'^', include('common.urls')),
    (r'^', include('main.urls')),
    (r'^inventory/', include('inventory.urls')),
    (r'^assets/', include('assets.urls')),
    (r'^search/', include('dynamic_search.urls')),
    (r'^import/', include('importer.urls')),
    (r'^movements/', include('movements.urls')),
    (r'^generic_photos/', include('photos.urls')),    
)

if settings.DEVELOPMENT:
    urlpatterns += patterns('',
        (r'^django-inventory-site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'site_media', 'show_indexes': True}),
    )

    if 'rosetta' in settings.INSTALLED_APPS:
        urlpatterns += patterns('',
            url(r'^rosetta/', include('rosetta.urls'), name = "rosetta"),
        )
