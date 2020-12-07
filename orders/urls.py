from django.conf.urls import url
from . import views
# Your urlpatterns here
urlpatterns = [
    url(r'^ord/$', views.OrderList.as_view(), name="order_list"),
    url(r'^create/$', views.order_create, name='order_create'),
    url(r'^admin/order/(?P<order_id>\d+)/$', views.admin_order_detail, name='admin_order_detail'),
    url(r'^admin/order/(?P<order_id>\d+)/pdf/$', views.admin_order_pdf, name='admin_order_pdf'),
    url(r'^payment/$', views.payment, name='payment'),
]
