from authtools.admin import BASE_FIELDS, SIMPLE_PERMISSION_FIELDS
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class MockRequest:
    pass


request = MockRequest()


class AccountsAdminTestCase(TestCase):

    def setUp(self):
        user = User.objects.create_user(
            email="testuser@test.com",
            password="test1234test"
        )
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
        self.user = user
        self.site = AdminSite()

    def test_user_in_admin(self):
        self.assertTrue(User in admin.site._registry)

    def test_modeladmin_str(self):
        model_admin = ModelAdmin(User, self.site)
        self.assertEqual(str(model_admin), 'accounts.ModelAdmin')

    def test_fields(self):
        model_admin = ModelAdmin(User, self.site)
        self.assertEqual(list(model_admin.get_form(request).base_fields), [
            'password',
            'last_login',
            'is_superuser',
            'groups',
            'user_permissions',
            'is_removed',
            'email',
            'is_staff',
            'is_active',
            'date_joined',
            'name'
        ])
        self.assertEqual(list(model_admin.get_fields(request)), [
            'password',
            'last_login',
            'is_superuser',
            'groups',
            'user_permissions',
            'is_removed',
            'email',
            'is_staff',
            'is_active',
            'date_joined',
            'name'
        ])
        self.assertEqual(list(model_admin.get_fields(request, self.user)), [
            'password',
            'last_login',
            'is_superuser',
            'groups',
            'user_permissions',
            'is_removed',
            'email',
            'is_staff',
            'is_active',
            'date_joined',
            'name'
        ])
        self.assertIsNone(model_admin.get_exclude(request, self.user))

    def test_fieldsets(self):
        model_admin = ModelAdmin(User, self.site)
        self.assertEqual(
            model_admin.get_fieldsets(request),
            [(None, {'fields': [
                'password',
                'last_login',
                'is_superuser',
                'groups',
                'user_permissions',
                'is_removed',
                'email',
                'is_staff',
                'is_active',
                'date_joined',
                'name'
            ]})]
        )
        self.assertEqual(
            model_admin.get_fieldsets(request, self.user),
            [(None, {'fields': [
                'password',
                'last_login',
                'is_superuser',
                'groups',
                'user_permissions',
                'is_removed',
                'email',
                'is_staff',
                'is_active',
                'date_joined',
                'name'
            ]})]
        )
