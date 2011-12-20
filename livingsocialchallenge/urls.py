from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

#define which pages will get loaded for which URL
urlpatterns = patterns('',
	url(r'^upload/$', 'upload.views.upload'),
	url(r'^$', 'upload.views.upload'),
    url(r'^admin/', include(admin.site.urls)),
)
