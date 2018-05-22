import uuid as uuid_lib

from django.db import models


class UniversallyUniqueIdentifiable(models.Model):
    uuid = models.UUIDField(
        db_index=True,
        default=uuid_lib.uuid4,
        editable=False
    )

    class Meta:
        abstract = True
