from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = CustomUser

    list_display = ['first_name', 'last_name', 'email', 'is_staff']
    list_filter = ['is_staff', 'is_superuser', 'is_active']
    search_fields = ['first_name', 'last_name', 'email']
    ordering = ['first_name', 'last_name']

    fieldsets = (
        ('User', {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'is_staff', 'is_superuser'),
        }),
    )

    def get_queryset(self, request):
            # If the user is a superuser, show all users
            if request.user.is_superuser:
                return super().get_queryset(request)
            # Otherwise, filter out superusers
            return super().get_queryset(request).filter(is_superuser=False)