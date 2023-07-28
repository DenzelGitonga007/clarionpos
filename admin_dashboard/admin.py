from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import User
from accounts import admin
from inventory import admin
from inventory.models import Store, Category, Product


# from admin_dashboard.models import Report

# # Register the models from the accounts app
# class CustomUserAdmin(UserAdmin):
#     model = User
#     list_display = ['username', 'email', 'is_staff', 'is_superuser']
#     fieldsets = (
#         (None, {'fields': ('username', 'email', 'password')}),
#         ('Permissions', {'fields': ('is_staff', 'is_active')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
#         ),
#     )
#     search_fields = ('username', 'email')
#     ordering = ('username',)
    
# class StoreAdmin(admin.ModelAdmin):
#     # Customize the display of fields in the admin list view
#     list_display = ['name']  # Add any other fields you want to display
    
#     # Customize the search fields in the admin list view
#     search_fields = ['name']  # Add any other fields you want to search
    

# class CategoryAdmin(admin.ModelAdmin):
#     # Customize the display of fields in the admin list view
#     list_display = ['name']  # Add any other fields you want to display
    
#     # Customize the search fields in the admin list view
#     search_fields = ['name']  # Add any other fields you want to search
    

# class ProductAdmin(admin.ModelAdmin):
#     # Customize the display of fields in the admin list view
#     list_display = ['name', 'category', 'store']  # Add any other fields you want to display
    
#     # Customize the search fields in the admin list view
#     search_fields = ['name']  # Add any other fields you want to search




# Register user admin model
# admin.site.register(User, CustomUserAdmin)
# Register the models from the inventory app
# admin.site.register(Store)
# admin.site.register(Category)
# admin.site.register(Product)

# Register the models from the admin_dashboard app
# admin.site.register(Report)
