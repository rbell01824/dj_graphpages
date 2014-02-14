from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dj_graphpages.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^import_baby_names/', include('baby_names.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
