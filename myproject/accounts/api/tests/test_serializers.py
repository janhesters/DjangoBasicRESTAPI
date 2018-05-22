from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from ..serializers import TokenSerializer, UserDetailSerializer

User = get_user_model()


class AccountsAPISerializerTestCase(APITestCase):

    def setUp(self):
        user = User.objects.create_user(
            email="testuser@test.com",
            password="test1234",
            name="Test User"
        )
        token, created = Token.objects.get_or_create(user=user)
        self.user = user
        self.token = token
        self.userserializer = UserDetailSerializer(instance=self.user)
        self.tokenserializer = TokenSerializer(instance=self.token)

    def test_userserializer_contains_fields(self):
        """Test if userserializer has it's expected fields."""
        data = self.userserializer.data
        self.assertCountEqual(set(data.keys()), set(['uuid', 'name']))

    def test_tokenserializer_contains_fields(self):
        """Test if tokenserializer has it's expected fields."""
        data = self.tokenserializer.data
        self.assertCountEqual(set(data.keys()), set(['key', 'user']))

    def test_userserializer_field_content(self):
        """Test if userserializer produces expected data."""
        data = self.userserializer.data
        self.assertEqual(data['name'], self.user.name)
        self.assertEqual(data['uuid'], str(self.user.uuid))

    def test_tokenserializer_field_content(self):
        """Test if tokenserializer produces expected data."""
        data = self.tokenserializer.data
        self.assertEqual(data['key'], self.token.key)
        self.assertEqual(data['user'], self.userserializer.data)
