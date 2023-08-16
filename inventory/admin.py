from django.contrib import admin
from .models import Store, Category, Product, Stock, Customer, PaymentMethod


class StockInline(admin.StackedInline):
    model = Stock
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'pieces_per_carton']
    search_fields = ['name']
    inlines = [StockInline]


class StockAdmin(admin.ModelAdmin):
    list_display = ['store', 'product', 'quantity', 'get_total_cartons']
    list_filter = ['store']
    search_fields = ['product__name']

    def get_total_cartons(self, obj):
        total_cartons, remaining_pieces = obj.get_total_cartons_and_pieces()
        return f"{total_cartons} cartons {remaining_pieces} pieces"
    get_total_cartons.short_description = 'Quantity'

    def save_model(self, request, obj, form, change):
        # Check if a stock entry already exists for the product in the store
        try:
            stock = Stock.objects.get(store=obj.store, product=obj.product)
            # Stock entry already exists, update the quantity
            stock.quantity += obj.quantity
            stock.save()
        except Stock.DoesNotExist:
            # Stock entry does not exist, create a new entry
            super().save_model(request, obj, form, change)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone_number', 'location']
    search_fields = ['name', 'phone_number', 'location']

class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['name',]
    search_fields = ['name',]

admin.site.register(Store)
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(PaymentMethod, PaymentMethodAdmin)
