from django.conf.urls import patterns, url

from scrape import views

urlpatterns = patterns('', url(r'^$', views.index, name='index'),)
