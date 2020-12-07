from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.http.response import HttpResponse
from .models import ReceivedNote, ReceivedAdviceNote, Material
from river.models import State

# Create your views here.


@staff_member_required
def goods_received_note(request, received_note_id):
    rec_note = get_object_or_404(ReceivedNote, pk=received_note_id)
    notes = ReceivedNote.objects.get(pk=received_note_id)
    received_note = notes.receivednote.all()
    return render(request, 'admin/received_note/received_note.html',
                  {'rec_note': rec_note, 'received_note': received_note})


@staff_member_required
def goods_received_advice_note(request, received_advice_note_id):
    rec_note = get_object_or_404(ReceivedAdviceNote, id=received_advice_note_id)
    notes = ReceivedAdviceNote.objects.get(pk=received_advice_note_id)
    received_advice_note = notes.receivedadvicenote.all()
    return render(request, 'admin/received_advice_note/received_advice_note.html',
                  {'rec_note': rec_note, 'received_advice_note': received_advice_note})


def process_received_note(request, note_id, next_state_id=None):
    received_note = get_object_or_404(ReceivedNote, pk=note_id)
    next_state = get_object_or_404(State, pk=next_state_id)
    try:
        received_note.proceed(request.user, next_state=next_state)
        return redirect(reverse('admin:raw_materials_dept_receivednote_changelist'))
    except Exception as e:
        return HttpResponse(e)


def process_received_advice_note(request, advice_note_id, next_state_id=None):
    received_note = get_object_or_404(ReceivedAdviceNote, pk=advice_note_id)
    next_state = get_object_or_404(State, pk=next_state_id)
    try:
        received_note.proceed(request.user, next_state=next_state)
        return redirect(reverse('admin:raw_materials_dept_receivedadvicenote_changelist'))
    except Exception as e:
        return HttpResponse(e)
