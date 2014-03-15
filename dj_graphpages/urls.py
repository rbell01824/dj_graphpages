from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

from .views import index
from graphpages.views import GraphPageGraphListView
from graphpages.experiments import CrispyView, GraphFormX2View

urlpatterns = patterns('',
    url(r'^test_data/', include('test_data.urls')),
    url(r'^display_graph_pages$',
        GraphPageGraphListView.as_view(), name=GraphPageGraphListView),
    url(r'^graphpages/', include('graphpages.urls')),
    url(r'^demo/', include('chartkick_demo.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^crispy$', CrispyView.as_view(), name=CrispyView),
    url(r'^djangoforms$', GraphFormX2View.as_view(), name=GraphFormX2View),
    url(r'^$', index, name='index'),
)

urlpatterns += staticfiles_urlpatterns()