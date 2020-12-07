from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.models import Group
from django.contrib.admin.models import LogEntry, DELETION
from django.core.urlresolvers import reverse
from .models import Material, Manufacturer, ReceivedNote, ReceivedAdviceNote
from .forms import GoodsReceivedNoteForm, MaterialForm
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


class RawMaterialsAdminSite(AdminSite):
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
admin_site = RawMaterialsAdminSite(name='raw_dept_admin')


class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'phone', 'created','is_active')
    list_filter = ('is_active', 'created')
    icon = '<i class="material-icons">build</i>'
admin_site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)

"""
class GoodsReceivedInline(admin.StackedInline):
    model = ReceivedNote
    exclude = ('expiry_date', 'material', 'manufacture_date', 'product_name')
    extra = 1
    fk_name = 'material'
"""


class MaterialInline(admin.StackedInline):
    form = MaterialForm
    model = Material
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'manufacturer', 'expiry_date', 'quantity',
                    'unit_price')
    list_filter = ('expiry_date',)
    # list_editable = ('unit_price', 'quantity')
    search_fields = ['product_name', 'description']
    raw_id_fields = ['manufacturer']
    icon = '<i class="material-icons">widgets</i>'
    # inlines = [GoodsReceivedInline]
admin_site.register(Material, ProductAdmin)
admin.site.register(Material, ProductAdmin)


def received_note(obj):
    return '<a href="{}">View</a>'.format(reverse('raw_materials_dept:received_note',
                                                  args=[obj.id]))
received_note.allow_tags = True


class GoodsReceivedAdmin(admin.ModelAdmin):
    form = GoodsReceivedNoteForm
    list_display = ('batch_no', received_note,
                    'status', 'staff_actions')
    list_filter = ('status', 'approved')
    search_fields = ['batch_num']
    inlines = [MaterialInline]
    icon = '<i class="material-icons">assignment</i>'


    def get_list_display(self, request):
        self.user = request.user
        return super(GoodsReceivedAdmin, self).get_list_display(request)

    def staff_actions(self, obj):
        content = ""
        for proceeding in obj.get_available_proceedings(self.user):
            content += create_proceed_button(obj, proceeding)
        return content

    def save_model(self, request, obj, form, change):
        if change:
            obj.created_by = request.user
        else:
            obj.created_by = request.user
        obj.save()

    staff_actions.allow_tags = True

admin_site.register(ReceivedNote, GoodsReceivedAdmin)
admin.site.register(ReceivedNote, GoodsReceivedAdmin)


def received_advice_note(obj):
    return '<a href="{}">View</a>'.format(reverse('raw_materials_dept:received_advice_note',
                                                  args=[obj.id]))
received_advice_note.allow_tags = True


class GoodsReceivedAdviceAdmin(admin.ModelAdmin):
    list_display = ('batch_no',  'created_by', received_advice_note, 'status', 'staff_actions')
    list_filter = ('created', 'updated')
    # list_editable = ('unit_price', 'quantity')
    search_fields = ['batch_no']
    icon = '<i class="material-icons">assignment</i>'

    def get_list_display(self, request):
        self.user = request.user
        return super(GoodsReceivedAdviceAdmin, self).get_list_display(request)

    def staff_actions(self, obj):
        content = ""
        for proceeding in obj.get_available_proceedings(self.user):
            content += create_proceed_advice_button(obj, proceeding)
        return content

    def save_model(self, request, obj, form, change):
        if change:
            obj.created_by = request.user
        else:
            obj.created_by = request.user
        obj.save()

    staff_actions.allow_tags = True
admin_site.register(ReceivedAdviceNote, GoodsReceivedAdviceAdmin)
admin.site.register(ReceivedAdviceNote, GoodsReceivedAdviceAdmin)


class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'action_time'
    # readonly_fields = LogEntry._meta.get_all_field_names()

admin.site.register(LogEntry, LogEntryAdmin)