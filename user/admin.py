from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("개인 정보", {"fields": ("name", "nickname", "phone_number")}),
        ("권한",{"fields": ("is_active","is_admin","groups","user_permissions",)},),
    )

    readonly_fields = ("last_login", "created_at")

    add_fieldsets = (
        (None,
            {"classes": ("wide",),
            "fields": ("email", "nickname", "name", "password1", "password2"),},
        ),
    )

    list_display = ("email", "nickname", "name", "is_admin", "is_active")
    list_filter = ( "is_active", "is_admin")
    search_fields = ("email", "nickname", "name")
    ordering = ("-created_at",)
