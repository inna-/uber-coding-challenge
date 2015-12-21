from django.conf.urls import patterns, url

from food import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
)
