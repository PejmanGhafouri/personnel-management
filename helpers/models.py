import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from safedelete import HARD_DELETE
from safedelete.models import SafeDeleteModel


class BaseModel(SafeDeleteModel):
    _safedelete_policy = HARD_DELETE

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=_('Create Time'))
    modify_time = models.DateTimeField(auto_now=True, verbose_name=_('Modify Time'))
    auto_cols = ['create_time', 'modify_time', 'deleted']

    class Meta:
        ordering = ('-create_time',)
        get_latest_by = ('create_time',)
        abstract = True

    def save(self, keep_deleted=False, **kwargs):
        self.full_clean()
        return super().save(keep_deleted, **kwargs)
