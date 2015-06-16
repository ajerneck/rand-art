from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns(
    ''
    , url(r'^index/$', 'scrape.views.index')
    , url(r'^rate/$', 'scrape.views.rate')
)
