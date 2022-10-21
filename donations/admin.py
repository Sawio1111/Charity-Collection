from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


class UserAdmin(BaseUserAdmin):

	model = User
	list_display = ('email', 'is_admin', 'is_active',)
	list_filter = ('email', 'is_admin', 'is_active',)
	fieldsets = (
		(None, {'fields': ('email', 'password')}),
		('Permissions', {'fields': ('is_admin', 'is_active')}),
	)
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('email', 'password1', 'password2', 'is_admin', 'is_active')}
		 ),
	)
	search_fields = ('email',)
	ordering = ('email',)


admin.site.register(User, UserAdmin)