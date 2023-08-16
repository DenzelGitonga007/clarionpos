from django.contrib import admin
from .models import Sale, SaleItem, Expense


# Get transferred by value
def sold_by(obj):
    return obj.sold_by.username

# for saleitem
def items_sold_by(obj):
    return obj.sale.sold_by.username

# Get recorded_by for Expenses
def recorded_by(obj):
    return obj.recorded_by.username

class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1

class SaleAdmin(admin.ModelAdmin):
    inlines = [SaleItemInline]
    list_display = [sold_by, 'date', 'customer', 'total_amount', 'rendered_amount', 'balance', 'payment_method']
    search_fields = ['customer__name', 'customer__email', 'payment_method']
    list_filter = ['sold_by', 'date', 'payment_method']

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Only set transferred_by on creation, not on update
            obj.sold_by = request.user
        super().save_model(request, obj, form, change)

    # Customize the column header for transferred_by
    sold_by.short_description = 'Sold By'

class SaleItemAdmin(admin.ModelAdmin):
    list_display = [items_sold_by, 'product', 'quantity', 'unit', 'sale_price']
    list_display_links = [items_sold_by]


# Expenses
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['date', 'description', 'amount', 'store', recorded_by]
    list_filter = ['date', 'store', 'description']
    search_fields = [recorded_by, 'store', 'description', 'store']
    def save_model(self, request, obj, form, change):
        if not obj.recorded_by:
            obj.recorded_by = request.user
        super().save_model(request, obj, form, change)
 
admin.site.register(Sale, SaleAdmin)
admin.site.register(SaleItem, SaleItemAdmin)
admin.site.register(Expense, ExpenseAdmin)