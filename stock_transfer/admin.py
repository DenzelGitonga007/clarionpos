from django.contrib import admin
from . models import StockTransfer, TransferItem
# Get transferred by value
def transferred_by(obj):
    return obj.transferred_by.username

class TransferItemInline(admin.TabularInline):
    model = TransferItem
    extra = 1


class StockTransferAdmin(admin.ModelAdmin):
    inlines = [TransferItemInline]
    list_display = ['source_store', 'destination_store', transferred_by, 'transfer_time']

    # Save the stock transfer by the user who's logged in
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Only set transferred_by on creation, not on update
            obj.transferred_by = request.user
        super().save_model(request, obj, form, change)

    # Customize the column header for transferred_by
    transferred_by.short_description = 'Transferred By'

class TransferItemAdmin(admin.ModelAdmin):
    list_display = ['transfer', 'product', 'quantity']


admin.site.register(TransferItem, TransferItemAdmin)
admin.site.register(StockTransfer, StockTransferAdmin)
