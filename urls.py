from django.conf.urls import patterns, url

from silent_auction import views

urlpatterns = patterns('',
    url(r'^$', views.main_page, name = 'main'),
    url(r'^auction/(?P<auction_id>.*)/$', views.auction, name = 'auction'),
    url(r'^bid/$', views.bid_form, name = 'bid_form'),
    url(r'^bid/(?P<bid_id>.*)/$', views.bid_page, name = 'bid'),
    url(r'^api/auction/(?P<auction_id>.*)/$', views.api_price_check, name = 'price_check'),
)
