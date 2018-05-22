from authtools.admin import (BASE_FIELDS, SIMPLE_PERMISSION_FIELDS,
                             NamedUserAdmin)
from django.contrib import admin

from .models import User


def verified(obj):
    email = obj.emailaddress_set.filter(primary=True)
    if email.exists():
        return email[0].verified
    return False


verified.boolean = True


@admin.register(User)
class SoftDeletableNamedUserAdmin(NamedUserAdmin):
    """
    Overwrite the fields of the NamedUserAdmin to add is_removed.
    """

    date_hierarchy = "date_joined"
    list_display = (
        'email',
        'name',
        verified,
        'is_active',
        'is_removed',
    )
    search_fields = ["email", "name"]
    readonly_fields = ("date_joined", "modified")
    fieldsets = (
        BASE_FIELDS,
        SIMPLE_PERMISSION_FIELDS,
        ("Contact information", {
            "fields": (
                ("email", "name")
            )
        }),
        ("Account information", {
            "fields": (
                "is_removed",
            ),
        }),
        ("Dates", {
            "fields": (
                ("date_joined", "modified"),
            ),
        })
    )
    list_filter = ('is_active', 'is_removed',)
