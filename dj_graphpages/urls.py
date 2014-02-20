from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from .views import index
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dj_graphpages.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^test_data/', include('test_data.urls')),
    url(r'^demo/', include('chartkick_demo.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', index, name='index'),
)

urlpatterns += staticfiles_urlpatterns()