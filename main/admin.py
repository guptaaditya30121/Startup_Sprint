from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from .models import User, Contest, Domain, Handle
from django.forms import Textarea

# Register your models here.


class UserAdminConfig(UserAdmin):
    model = User
    search_fields = ('email', 'username')
    list_filter = ('email', 'username',
                   'streak', 'is_superuser')
    # ordering = ('-date_joined',)
    list_display = ('email', 'username',
                    'is_active', 'is_staff', 'id', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password', 'contest_history', 'domain', 'handles',
         'streak')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username',
                       'streak', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser')}
         ),
    )


admin.site.register(User, UserAdminConfig)
admin.site.register(Contest)
admin.site.register(Domain)
admin.site.register(Handle)
