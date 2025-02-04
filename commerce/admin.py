from django.contrib import admin
from django.contrib.auth.models import User, Group
from import_export.admin import ImportExportModelAdmin, ImportExportMixin
from commerce.models import *
from django.utils.html import format_html
from adminsortable2.admin import SortableAdminMixin
from import_export import resources

# Register your models here.

admin.site.register(Customer)
admin.site.register(Order)
# admin.site.register(Order)
admin.site.register(OrderItem)
# admin.site.register(Image)


class ImageInline(admin.TabularInline):
    model = Image
    extra = 3

class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock')
    search_fields = ('name', 'price')
    inlines = [ImageInline]
    list_filter = ['category', 'quantity', 'rating']
    autocomplete_fields = ['category']

admin.site.register(Product, ProductAdmin)

class ProductInline(admin.TabularInline):
    model = Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'product_count')
    search_fields = ('title',)

    inlines = [
        ProductInline,
    ]

    def product_count(self, category):
        return category.products.count()


admin.site.site_header = 'Alibaba Admin'
admin.site.site_title = 'Alibaba Admin Portal'
admin.site.index_title = 'Welcome To Alibaba Researcher Portal'