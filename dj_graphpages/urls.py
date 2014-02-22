from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

from .views import index
from graphpages.views import GraphListView
import forms_builder.forms.urls

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dj_graphpages.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^test_data/', include('test_data.urls')),
    url(r'^display_graph_pages$',
        GraphListView.as_view(), name=GraphListView),
    url(r'^graphpages/', include('graphpages.urls')),
    url(r'^demo/', include('chartkick_demo.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^forms/', include(forms_builder.forms.urls)),
    url(r'^forms2/', include('form_designer.urls')),
    url(r'^$', index, name='index'),
)

urlpatterns += staticfiles_urlpatterns()