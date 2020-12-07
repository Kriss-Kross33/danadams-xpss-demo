from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^admin/received_note/(?P<received_note_id>\d+)/$', views.goods_received_note,
        name='received_note'),
    url(r'^admin/received_advice_note/(?P<received_advice_note_id>\d+)/$',
        views.goods_received_advice_note, name='received_advice_note'),

    url(r'^process_note/(?P<note_id>\d+)/(?P<next_state_id>\d+)/$',
        views.process_received_note, name='process_note'),

    url(r'^process_advice_note/(?P<advice_note_id>\d+)/(?P<next_state_id>\d+)/$',
        views.process_received_advice_note, name='process_advice_note'),
]
