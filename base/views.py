from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse
from .models import Ticket
from river.models import State
# Create your views here


def proceed_ticket(request, ticket_id, next_state_id=None):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    next_state = get_object_or_404(State, pk=next_state_id)
    try:
        ticket.proceed(request.user, next_state=next_state)
        return redirect(reverse('admin:base_ticket_changelist'))
    except Exception as e:
        return HttpResponse(e)

