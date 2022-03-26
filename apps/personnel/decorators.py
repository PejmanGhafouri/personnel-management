from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext as _

from apps.personnel.models import Permission

User = get_user_model()


def required_permissions(permissions=None):
    if permissions is None:
        permissions = []

    def decorator(view_func):
        def wrap(request, *args, **kwargs):
            if request.user.is_authenticated:
                user_permissions = Permission.objects.filter(role__users=request.user).values_list('code', flat=True)
                has_permission = False
                for permission_list in permissions:
                    if set(permission_list).intersection(set(user_permissions)) == set(permission_list):
                        has_permission = True
                if not has_permission:
                    raise PermissionDenied(_('You do not have access to this page'))

            return view_func(request, *args, **kwargs)

        return wrap

    return decorator


class RequiredPermissionsMixin:
    permission_required = []
    permission_denied_message = ''

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            permission = Permission.objects.filter(role__users=self.request.user).values_list('code', flat=True)
            has_permission = False
            for permission_list in self.permission_required:
                if set(permission_list).intersection(set(permission)) == set(permission_list):
                    has_permission = True
            if not has_permission:
                raise PermissionDenied(_(self.permission_denied_message))

        return super().dispatch(request, *args, **kwargs)
