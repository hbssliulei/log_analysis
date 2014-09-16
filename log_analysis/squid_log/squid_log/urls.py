from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from web01.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'squrid_log.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
	url(r'^$',index),
	url(r'^login/$',login),
	url(r'^get_log_data/$',get_log_data)
)
