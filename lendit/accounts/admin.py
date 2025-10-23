from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import CustomUser

admin.site.site_header = "LendIt Admin"
admin.site.site_title = "LendIt Admin"
admin.site.index_title = "LendIt Site Administration"


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    # Which forms admin will use when adding or displaying the
    # user model in the admin site.
    #
    # The display form in this case is also an update form so we
    # can edit from within the admin site
    add_form = UserCreationForm
    form = UserChangeForm
    model = CustomUser

    list_display = ["first_name", "last_name", "email", "is_staff", "is_active"]
    list_filter = ["is_staff", "is_active", "is_superuser"]
    search_fields = ["first_name", "last_name", "email"]
    ordering = ["first_name", "last_name"]

    # The fields that are present for the model in the admin site
    fieldsets = (
        ("User", {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important Dates", {"fields": ("last_login",)}),
    )

    # The fields used in the admin form for adding new users
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )

    def get_queryset(self, request):
        # If the user is a superuser, show all users
        if request.user.is_superuser:
            return super().get_queryset(request)
        # Otherwise, filter out superusers
        return super().get_queryset(request).filter(is_superuser=False)
