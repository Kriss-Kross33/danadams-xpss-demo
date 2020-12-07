from django.contrib import admin
from django.contrib.admin import AdminSite
from django.core.urlresolvers import reverse
from .models import Product, MaterialsRequired
from django.contrib.auth.models import Group
from django.contrib.admin.models import LogEntry, DELETION
from django import forms
from .forms import MaterialsRequiredInlineForms
# Register your models here.


def create_proceed_button(obj, proceeding):
    return """
        <input type="button"
        class="btn btn-primary"
        style="margin:2px 2px 2px 2px;"
        value="{0}"
        onclick="location.href='{1}'"/>
    """.format(proceeding.meta.transition,
               reverse('raw_materials_dept:process_note',
                       kwargs={'note_id': obj.pk,
                               'next_state_id': proceeding.meta.transition.destination_state.pk}))


def create_proceed_advice_button(obj, proceeding):
    return"""
        <input type="button"
        class="btn btn-primary"
        style="margin:2px 2px 2px 2px;"
        value="{0}"
        onclick="location.href='{1}'"/>
    """.format(proceeding.meta.transition,
               reverse('raw_materials_dept:process_advice_note',
                       kwargs={'advice_note_id': obj.pk,
                               'next_state_id': proceeding.meta.transition.destination_state.pk}))


class ProductionAdminSite(AdminSite):
    site_header = 'Raw Materials Department'
    site_title = 'Danadams Pharmaceuticals'
    index_title = 'Danadams Pharmaceuticals'

    def has_permission(self, request):
        """
        Check to see if user is either a superuser or a member of the
        Raw Department
        :param request:
        :return:
        """
        raw_mat_officers_grp = Group.objects.get(name='RAW MATERIALS STORE OFFICERS')
        raw_mat_supervisor_grp = Group.objects.get(name='HEAD OF RAW MATERIALS DEPT')
        return raw_mat_officers_grp in request.user.groups.all() or raw_mat_supervisor_grp in \
                                                                    request.user.groups.all()
admin_site = ProductionAdminSite(name='prod_dept_admin')


def received_note(obj):
    return '<a href="{}">View</a>'.format(reverse('raw_materials_dept:received_note',
                                                  args=[obj.id]))
received_note.allow_tags = True


class MaterialsRequiredInline(admin.StackedInline):
    form = MaterialsRequiredInlineForms
    model = MaterialsRequired
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'batch_no', 'batch_size', 'manufacture_date', 'created', 'staff_actions')
    list_filter = ('manufacture_date', 'created', 'updated')
    inlines = (MaterialsRequiredInline,)
    icon = '<i class="material-icons">assignment</i>'

    def get_list_display(self, request):
        self.user = request.user
        return super(ProductAdmin, self).get_list_display(request)

    def staff_actions(self, obj):
        content = ""
        for proceeding in obj.get_available_proceedings(self.user):
            content += create_proceed_button(obj, proceeding)
        return content

    staff_actions.allow_tags = True
admin_site.register(Product, ProductAdmin)
admin.site.register(Product, ProductAdmin)


class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'action_time'
    # readonly_fields = LogEntry._meta.get_all_field_names()
admin_site.register(LogEntry, LogEntryAdmin)

