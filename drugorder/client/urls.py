from django.conf.urls import include, url
from django.conf.urls import *
from django.contrib import admin
from .views import client_create,order_create,order_confirm,order_list,index
urlpatterns = [
    url(r'^$',index, name="home"),
    url(r'^order_history/$',order_list, name="order_history"),
    url(r'^order_confirmation/$',order_confirm, name="order_confirm"),
    url(r'^client_form/$',client_create, name="client_form"),
    url(r'^make_order/$',order_create, name="make_order"),
    url(r'^admin/', admin.site.urls)
]