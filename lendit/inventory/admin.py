from django.contrib import admin
from django.utils.html import format_html

from django_summernote.admin import SummernoteModelAdmin


from .models import Item, BorrowEvent
from .forms import ItemAdminForm



class BorrowEventInline(admin.TabularInline):
    model = BorrowEvent
    extra = 0
    readonly_fields = ('user', 'borrowed_at', 'returned_at')
    verbose_name = "Transaction"
    verbose_name_plural = "Transactions"

@admin.register(Item)
class ItemAdmin(SummernoteModelAdmin):
    form = ItemAdminForm
    show_facets = admin.ShowFacets.ALWAYS

    summernote_fields = ('description',)

    inlines = [BorrowEventInline]
    list_display = ['name', 'status','display_tags', 'replacement_link', 'price', 'borrower', 'is_hidden']
    list_filter = ['status', 'tags', 'is_hidden']
    search_fields = ['name',  'status', 'borrower__email', 'borrower__first_name', 'borrower__last_name', 'tags__name']
    ordering = ['name', 'status', 'tags', 'created_at', 'updated_at', 'last_borrowed_at', 'checked_in_at']

    readonly_fields = ('created_at', 'updated_at', 'last_borrowed_at', 'checked_in_at', 'image_preview')

    def get_fieldsets(self, request, obj=None):
        if obj:
            return (
                    ('Item Details', {
                        'classes' : ('wide',),
                        'fields': ('name', 'image_preview', 'image', 'price', 'description' , 'replacement_link', 'tags', )
                        }),
                    ('Item Status', {
                        'classes' : ('wide',),
                        'fields': ('status', 'is_hidden', 'borrower')
                        }),
                    ('Important Dates', {
                        'classes' : ('collapse',),
                        'fields': ('created_at', 'updated_at', 'last_borrowed_at', 'checked_in_at')
                        }),
                    )
        else:
            return (None, {
            'classes': ('wide',),
            'fields': ('name', 'image', 'price', 'description', 'replacement_link',  'tags', 'status', 'is_hidden'),
        }),

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields
        return []


    def image_preview(self, item):
        if item.image:
            return format_html('<img src="{}" style="max-height: 200px;" />', item.image.url)
        return "No image"
    
    
    def display_tags(self, obj):
        return ", ".join(o.name for o in obj.tags.all())
    
    display_tags.short_description = 'Tags'
    image_preview.short_description = 'Preview'


admin.site.register(BorrowEvent)