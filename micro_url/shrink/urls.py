from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^mu/', views.redirect, name='redirect'),
    url(r'^$', views.create_micro_url, name='create_micro_url'),
    url(r'^display/(?P<pk>[0-9]+)/$',
        views.display_micro_url, name='display_micro_url'),
    url(r'^preview/(?P<pk>[0-9]+)/$',
        views.preview_micro_url, name='preview_micro_url')
]
