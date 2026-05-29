from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Admin configuration for CustomUser."""
    list_display = ('username', 'email', 'channel_name', 'is_staff', 'created_at')
    search_fields = ('username', 'email', 'channel_name')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'created_at')
    
    # Add custom fields to fieldsets
    fieldsets = UserAdmin.fieldsets + (
        ('MiniTune Info', {'fields': ('channel_name', 'avatar', 'bio')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('MiniTune Info', {'fields': ('channel_name', 'avatar', 'bio')}),
    )
