from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'store', 'email', 'is_staff', 'is_superuser']
    fieldsets = (
        (None, {'fields': ('username', 'store', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'store', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username', 'store', 'email')
    ordering = ('username',)

admin.site.register(User, CustomUserAdmin)
