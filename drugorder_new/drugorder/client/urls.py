from django.conf.urls import include, url
from django.conf.urls import *
from django.contrib import admin
from .views import client_create,order_create,order_confirm,order_list,index,test_order,product_search,dautocomplete,completed_order,shopping_cart,wish_revise,recent_order
urlpatterns = [
    url(r'^$',index, name="home"),
    url(r'^recent_order/$',recent_order, name="recent_order"),
    url(r'^completed_order/$',completed_order, name="completed_order"),
    url(r'^order_history/$',order_list, name="order_history"),
    url(r'^shopping_cart/$', shopping_cart, name="shopping_cart"),
    url(r'^order_confirmation/$',order_confirm, name="order_confirm"),
    url(r'^client_form/$',client_create, name="client_form"),
    url(r'^make_order/$',order_create, name="make_order"),
    url(r'^test_order/$',test_order, name="test_order"),
    url(r'^product_search/$',product_search, name="product_search"),
    url(r'^dautocomplete/$',dautocomplete, name="dautocomplete"),
    url(r'^wish_revise/$',wish_revise, name="wish_revise"),
    url(r'^admin/', admin.site.urls)
]