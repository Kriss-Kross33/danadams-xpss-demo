from django.contrib import admin
from django.core.urlresolvers import reverse
from .models import Ticket


def create_proceed_button(obj, proceeding):
    return """
        <input type="button"
        class="btn btn-primary"
        style="margin:2px 2px 2px 2px;"
        value="{0}"
        onclick="location.href='{1}'"/>
    """.format(proceeding.meta.transition,
               reverse('base:proceed_ticket',
                       kwargs={'note_id': obj.pk,
                               'next_state_id': proceeding.meta.transition.destination_state.pk}))


class TicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_num', 'status', 'staff_actions')
    search_fields = ('ticket_num',)

    def get_list_display(self, request):
        self.user = request.user
        return super(TicketAdmin, self).get_list_display(request)

    def staff_actions(self, obj):
        content = ""
        for proceeding in obj.get_available_proceedings(self.user):
            content += create_proceed_button(obj, proceeding)
        return content

    staff_actions.allow_tags = True
admin.site.register(Ticket, TicketAdmin)

