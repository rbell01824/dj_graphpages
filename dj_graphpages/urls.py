from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

from .views import index
from graphpages.views import GraphPageGraphListView
from graphpages.crispyexperiments import CrispyView
import forms_builder.forms.urls

urlpatterns = patterns('',
    url(r'^test_data/', include('test_data.urls')),
    url(r'^display_graph_pages$',
        GraphPageGraphListView.as_view(), name=GraphPageGraphListView),
    url(r'^graphpages/', include('graphpages.urls')),
    url(r'^demo/', include('chartkick_demo.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^forms/', include(forms_builder.forms.urls)),
    url(r'^forms2/', include('form_designer.urls')),
    url(r'^crispy$', CrispyView.as_view(), name=CrispyView),
    url(r'^$', index, name='index'),
)

urlpatterns += staticfiles_urlpatterns()