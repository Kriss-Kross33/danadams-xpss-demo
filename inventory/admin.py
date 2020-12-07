from django.contrib import admin
from .models import Product, Category, Vendor
from .forms import PageForm

# TODO: Customize the admin interface
# TODO: GEnerate receipt
# TODO: Generate PDF invoice upon payment


class PageAdmin(admin.ModelAdmin):
    form = PageForm
    fieldsets = [
      ('Body', {'classes': ('full-width',), 'fields': ('body',)})
    ]


class ProductAdmin(admin.ModelAdmin):
    form = PageForm
    date_hierarchy = 'date_added'
    """
    fieldsets = [
        (None, {'fields': ['name', 'slug', 'chem_formula', 'category']}),
        ('Vendor Information', {'fields': ['vendor', 'catalog', 'manufacturer',
                                           'manufacturer_number',
                                           'size', 'unit',]}),
        (None, {'fields': ['parent_item', 'comments']})
    ]
    """
    list_display = ('name', 'price', 'stock', 'expiry', 'category', 'date_updated')
    list_filter = ('category' ,'date_added')
    list_editable = ('price', 'stock')
    search_fields = ('name', 'chem_formula', 'manufacturer_number', 'description')
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Product, ProductAdmin)


class CategoryAdmin(admin.ModelAdmin):
    form = PageForm
    list_display = ('name', 'slug', 'created', 'updated', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('parent', 'created',)
    search_fields = ('name', 'description',)
    date_hierarchy = 'created'
admin.site.register(Category, CategoryAdmin)

    


