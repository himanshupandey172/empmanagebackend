from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from django.contrib import admin, messages


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "email",
                    "first_name",
                    "last_name",
                ),
            },
        ),
    )


admin.site.site_header = "Lemon robotics Admin"
admin.site.index_title = "Admin"
