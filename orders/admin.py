import csv
import datetime
from django.contrib import admin
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from .models import Order, OrderItem, PaymentMethod


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(opts.verbose_name)
    writer = csv.writer(response)

    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    # write the header row
    writer.writerow([field.name for field in fields])
    # write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response
export_to_csv.short_description = 'Export to CSV'


def order_detail(obj):
    return '<a href="{}">View</a>'.format(reverse('orders:admin_order_detail',
                                                  args=[obj.id]))
order_detail.allow_tags = True


class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 1


class OrderItemAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_arrived'
    fields = ('product', 'quantity', 'price', 'date_arrived', 'serial',
              'location', 'expiry_years', 'reconciled')
    list_display = ('order_date', 'date_arrived', 'price', 'location')
    list_filter = ('order__order_date', 'date_arrived', 'location')
    raw_id_fields = ['product']
admin.site.register(OrderItem, OrderItemAdmin)


def order_pdf(obj):
    return '<a href="{}">PDF</a>'.format(reverse('orders:admin_order_pdf',
                                                 args=[obj.id]))
order_pdf.allow_tags = True
order_pdf.short_description = 'PDF bill'


class ViewAdmin(admin.ModelAdmin):

    """
    Custom made change_form template just for viewing purposes
    You need to copy this from /django/contrib/admin/templates/admin/change_form.html
    And then put that in your template folder that is specified in the
    settings.TEMPLATE_DIR
    """
    change_form_template = 'view_form.html'

    # Remove the delete Admin Action for this Model
    actions = None

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        #Return nothing to make sure user can't update any data
        pass


class OrderAdmin(admin.ModelAdmin):
    date_hierarchy = 'order_date'
    fields = ('vendor', 'fullname', 'email', 'contact_number', 'delivery_address', 'location',
              'order_date', 'ordered', 'paid')
    list_display = ['id', 'vendor', 'fullname', 'location', 'order_date', 'paid',
                    'sales_person', order_detail, order_pdf]
    list_editable = ['sales_person']
    list_filter = ('ordered', 'vendor', 'paid')
    raw_id_fields = ('sales_person',)
    search_fields = ('fullname',)
    inlines = [OrderItemInline]
    actions = [export_to_csv]

    def queryset(self, request):
        """
        Limit models to those that belong to the request's User
        :param request:
        :return:
        """
        qs = super().queryset(request)
        if request.user.is_superuser:
            # return everything
            return qs
        
admin.site.register(Order, OrderAdmin)


class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active',)
    list_filter = ('is_active',)
    search_fields = ('name',)
    date_hierarchy = 'created_on'
admin.site.register(PaymentMethod, PaymentMethodAdmin)











