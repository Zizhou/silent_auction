from django.conf.urls import patterns, url

from silent_auction import views

urlpatterns = patterns('',
    url(r'^$', views.main_page, name = 'main'),
)
