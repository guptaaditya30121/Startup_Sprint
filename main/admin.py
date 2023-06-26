from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from .models import User, Contest, Domain, Handle, Points, Time

# Register your models here.


class UserAdminConfig(UserAdmin):
    model = User
    search_fields = ('email', 'username')
    list_filter = ('email', 'username',
                   'user_points', 'is_superuser')
    # ordering = ('-date_joined',)
    list_display = ('email', 'username',
                    'is_active', 'is_staff', 'id', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('name','email', 'username', 'password', 'contest_history', 'domain',
         'user_points')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username',
                       'user_points', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser')}
         ),
    )


admin.site.register(User, UserAdminConfig)
admin.site.register(Contest)
admin.site.register(Domain)
admin.site.register(Handle)
admin.site.register(Points)
admin.site.register(Time)
