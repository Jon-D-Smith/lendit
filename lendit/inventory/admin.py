from django.contrib import admin
from django.utils.html import format_html

from django_summernote.admin import SummernoteModelAdmin
from taggit.admin import TagAdmin
from taggit.models import Tag, TaggedItem

from .models import Item, BorrowEvent, InventoryTag, InventoryTaggedItem
from .forms import ItemAdminForm


# Setting up the borrow event to be placeable inside the ItemAdmin view
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
    actions=["set_status_available", "set_status_lost", "set_status_needs_repair", "set_status_needs_replacing", "set_status_pending_checkin"]

    list_display = ['name', 'status','display_tags', 'replacement_link', 'price', 'borrower', 'is_hidden']
    list_filter = ['status', 'tags', 'is_hidden']
    search_fields = ['name',  'status', 'borrower__email', 'borrower__first_name', 'borrower__last_name', 'tags__name']
    ordering = ['name', 'status', 'tags', 'created_at', 'updated_at', 'last_borrowed_at', 'checked_in_at']

    readonly_fields = ('created_at', 'updated_at', 'last_borrowed_at', 'checked_in_at', 'image_preview')

    # Overriding the get_fieldsets to split the detail and add views
    def get_fieldsets(self, request, obj=None):
        # If the item already exists, render these fields
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
        # If the item does not exist we are making it. Render the add item form
        else:
            return (None, {
            'classes': ('wide',),
            'fields': ('name', 'image', 'price', 'description', 'replacement_link',  'tags', 'status', 'is_hidden'),
        }),

    # Only return readonly fields for the detail view
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields
        return []

    # Render the image in the the admin detail view
    def image_preview(self, item):
        if item.image:
            return format_html('<img src="{}" style="max-height: 200px;" />', item.image.url)
        return "No image"
    
    # display tags as a list in the listview
    def display_tags(self, obj):
        return ", ".join(o.name for o in obj.tags.all())
    



    #region Admin Acitons
    @admin.action(description="Set Item status to available")
    def set_status_available(self, request, queryset):
        queryset.update(status=Item.Status.AVAILABLE)

        self.message_user(request, "Success! Item(s) status set to available.")

    @admin.action(description="Set Item status to lost")
    def set_status_lost(self, request, queryset):
        queryset.update(status=Item.Status.LOST)

        self.message_user(request, "Success! Item(s) status set to lost.")

    @admin.action(description="Set Item status to needs repair")
    def set_status_needs_repair(self, request, queryset):
        queryset.update(status=Item.Status.REPAIR)

        self.message_user(request, "Success! Item(s) status set to needs repair.")
        
    @admin.action(description="Set Item status to needs replacing")
    def set_status_needs_replacing(self, request, queryset):
        queryset.update(status=Item.Status.REPLACE)

        self.message_user(request, "Success! Item(s) status set to needs replacing.")

    @admin.action(description="Set Item status to pending checkin")
    def set_status_pending_checkin(self, request, queryset):
        queryset.update(status=Item.Status.PENDING)

        self.message_user(request, "Success! Item(s) status set to pending checkin.")

    #endregion

    display_tags.short_description = 'Tags'
    image_preview.short_description = 'Preview'

@admin.register(InventoryTag)
class InventoryTagAdmin(TagAdmin):
    fieldsets = (
        ('Tag Info', {'fields': ('name','slug')}),
    )
    # Override the inline instances so it doesn't load the related tagged items
    def get_inline_instances(self, request, obj=None):
        return []

# @admin.register(InventoryTaggedItem)
# class InventoryTaggedItemAdmin(admin.ModelAdmin):
#     list_display = ['tag', 'content_type', 'object_id']


admin.site.register(BorrowEvent)

# Unregistering to built in Tag Model so we can use our proxy model
admin.site.unregister(Tag)