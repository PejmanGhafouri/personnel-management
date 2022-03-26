from django.contrib.admin import register

from helpers.admin import BaseAdmin
from .models import Contract, ContractComment, Role, Permission


@register(Contract)
class ContractAdmin(BaseAdmin):
    pass


@register(ContractComment)
class ContractCommentAdmin(BaseAdmin):
    pass


@register(Role)
class RoleAdmin(BaseAdmin):
    pass


@register(Permission)
class PermissionAdmin(BaseAdmin):
    pass
