from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from web01.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'squid_web.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    (r'^$', index ),
	(r'^get_squid_log/$', get_squid_log)
)
