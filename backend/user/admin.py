from django.contrib import admin
from .models import User as UserModel#, UserProfile as UserProfileModel, Hobby as HobbyModel
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin






class UserAdmin(BaseUserAdmin):
    list_display = ('login_id', 'username', 'email')
    list_display_links = ('login_id',)
    list_filter = ('login_id',)
    search_fields = ('login_id', 'email',)

    fieldsets = (
        ("info", {"fields": ("login_id", "password", "email", )}),
        ("Permissions", {"fields": ("is_admin", "is_active",)}),)

    filter_horizontal = []

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('login_id', 'join_data',)
        else:
            return ('join_data',)

admin.site.register(UserModel, UserAdmin)