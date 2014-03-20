from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login

from .views import index
from graphpages.views import GraphPageGraphListView
from graphpages.experiments import GraphFormX2View

urlpatterns = patterns('',
    url(r'^test_data/', include('test_data.urls')),
    url(r'^display_graph_pages$',
        GraphPageGraphListView.as_view(), name=GraphPageGraphListView),
    url(r'^graphpages/', include('graphpages.urls')),
    url(r'^demo/', include('chartkick_demo.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^djangoforms$', GraphFormX2View.as_view(), name=GraphFormX2View),
    url(r'^$', login_required(index), name='index'),
    url(r'^taggit_autosuggest/', include('taggit_autosuggest.urls')),
    url(r'^login/$', login, {'template_name': 'admin/login.html'})
)

urlpatterns += staticfiles_urlpatterns()