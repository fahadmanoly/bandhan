import imp
from django.contrib import admin
from useraccount.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


# Register your models here.

class UserModelAdmin(BaseUserAdmin):
    list_display = ["id","email", "name","tc","is_admin","is_phone_verified","is_block","is_gold","is_platinum"]
    list_filter = ["is_admin"]
    fieldsets = (
        ("User Credentials", {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("name","tc")}),
        ("Permissions", {"fields": ("is_admin","is_block","is_phone_verified","is_gold","is_platinum")}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserModelAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide"),
                "fields": ("email", "name", "tc", "password1", "password2"),
            }
        ),
    )
    search_fields = ("email","name")
    ordering = ("email","id")
    filter_horizontal = ()


# Now register the new UserModelAdmin...
admin.site.register(User, UserModelAdmin)



