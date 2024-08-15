from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from .models import User, UserResetPassword


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'id',
        'email',
    )
    list_display_links = ('id', 'email',)
    search_fields = ('first_name', 'email',)
    filter_horizontal = ('groups', 'user_permissions')
    list_filter = (
        'is_staff',
        'is_superuser',
        'is_active',
        'groups',
    )
    ordering = ('-date_joined',)
    fieldsets = (
        (None, {'fields': (
            'email',
            'password',
        )}),
        (_('Personal info'), {'fields': (
            'first_name',
        )}),
        (_('Permissions'), {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
        )}),
        (_('Important dates'), {'fields': (
            'date_joined',
            'last_login',
        )}),
    )
    readonly_fields = (
        'get_full_name',
        'date_joined',
        'last_login',
    )
    # autocomplete_fields = (
    #     'address',
    # )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
            ),
        }),
    )
