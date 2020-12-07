from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^proceed_ticket/(?P<ticket_id>\d+)/(?P<next_state_id>\d+)/$',
        views.proceed_ticket, name='proceed_ticket')
]