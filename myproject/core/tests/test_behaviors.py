import uuid

from django.db import connection
from django.db.models.base import ModelBase
from django.test import TestCase

from ..behaviors import UniversallyUniqueIdentifiable


class TestUniversallyUniqueIdentifiable(TestCase):

    model = UniversallyUniqueIdentifiable

    def setUp(self):
        # Create a dummy model
        self.model = ModelBase(
            '__TestModel__' + self.model.__name__, (self.model,),
            {'__module__': self.model.__module__}
        )

        # Create the schema for our test model
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(self.model)

    def test_uuid(self):

        self.model.objects.create(uuid=uuid.uuid4())
        self.assertEqual(self.model.objects.count(), 1)

    def tearDown(self):
        # Delete the schema for the test model
        with connection.schema_editor() as schema_editor:
            schema_editor.delete_model(self.model)
