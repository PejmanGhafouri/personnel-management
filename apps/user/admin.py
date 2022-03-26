from django.contrib import admin
from django.contrib.admin import register
from django.contrib.admin.utils import flatten_fieldsets
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from apps.personnel.models import Profile, Education, Bank, Spouse, Child

User = get_user_model()


class ProfileInline(admin.StackedInline):
    model = Profile


class BankInline(admin.StackedInline):
    model = Bank
    extra = 1


class EducationInline(admin.StackedInline):
    model = Education
    extra = 1


class SpouseInline(admin.StackedInline):
    model = Spouse
    extra = 1


class ChildInline(admin.StackedInline):
    model = Child
    extra = 1


@register(User)
class UserAdmin(UserAdmin):
    inlines = [ProfileInline, BankInline, EducationInline, SpouseInline, ChildInline]
    list_display = ('national_id', 'email', 'first_name', 'last_name', 'is_staff')
    fieldsets = (
        (None, {'fields': ('national_id', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Additional Data'), {'fields': ('phone_number',)}),
        (
            _('Permissions'),
            {
                'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            },
        ),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('national_id', 'password1', 'password2', 'phone_number'),
            },
        ),
    )
    search_fields = ('national_id', 'first_name', 'last_name', 'email', 'phone_number')
    ordering = ('national_id',)

    # def has_add_permission(self, request):
    #     return False
    #
    # def has_delete_permission(self, request, obj=None):
    #     return False
    #
    # def get_readonly_fields(self, request, obj=None):
    #     all_form_fields = flatten_fieldsets(self.get_fieldsets(request, obj))
    #     editable_fields = ['is_staff', 'groups', 'user_permissions']
    #
    #     read_only_fields = []
    #     for field in all_form_fields:
    #         if field not in editable_fields:
    #             read_only_fields.append(field)
    #
    #     return read_only_fields
