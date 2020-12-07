from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.coupon_apply, name='coupon_apply'),
]
