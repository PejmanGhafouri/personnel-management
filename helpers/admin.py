from django.utils.translation import gettext as _
from safedelete.admin import SafeDeleteAdmin
from .models import BaseModel


class BaseAdmin(SafeDeleteAdmin):
    list_display = ('__str__',)
    list_filter = ()

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        for col in BaseModel.auto_cols:
            try:
                fields.remove(col)
            except Exception:
                pass
        return fields

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        fieldsets += (
            (
                _('other data'),
                {
                    'fields': (
                        'create_time',
                        'modify_time',
                        'deleted',
                    )
                },
            ),
        )
        return fieldsets

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        return readonly_fields + ('create_time', 'modify_time', 'deleted')

    def get_list_filter(self, request):
        list_filter = super().get_list_filter(request)
        return list_filter + ('deleted',)

    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        return list_display + ('modify_time', 'deleted')
