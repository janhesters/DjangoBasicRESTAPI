from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token

User = get_user_model()


class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('name', 'uuid')
        read_only_fields = ('uuid',)


class TokenSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()

    class Meta:
        model = Token
        fields = ('key', 'user')
