from django.conf.urls import url

from inventory import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^products/$', views.product_list, name='product_list'),
    url(r'^(?P<category_slug>[-\w]+)/$', views.product_list, name='product_list_by_category'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.product_detail, name='product_detail'),

]
from django import apps

