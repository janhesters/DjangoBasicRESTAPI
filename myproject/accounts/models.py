from authtools.models import AbstractEmailUser, UserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.fields import AutoLastModifiedField
from model_utils.models import SoftDeletableModel

from core.behaviors import UniversallyUniqueIdentifiable


class User(
    UniversallyUniqueIdentifiable,
    SoftDeletableModel,
    AbstractEmailUser
):
    """
    User should generally not be deleted, but rather is_removed should just
    be set to true. The delete() method is overwritten in the
    SoftDeletableModel.
    Also add a uuid field to avoid displaying the sequential primary key.
    """

    name = models.CharField(_('name'), max_length=255, blank=True)
    modified = AutoLastModifiedField(_('modified'))

    objects = UserManager()
