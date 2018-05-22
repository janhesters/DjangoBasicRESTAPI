from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core import mail
from rest_framework import serializers, status
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse as api_reverse
from rest_framework.test import APITestCase

from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount, SocialApp
from config.settings.base import get_env_variable

User = get_user_model()


class AccountsAPIViewsTestCase(APITestCase):

    def setUp(self):
        user = User.objects.create_user(
            email="testuser@test.com",
            name="Test User",
            password="test1234test"
        )
        token, created = Token.objects.get_or_create(user=user)
        emailaddress = EmailAddress.objects.get_or_create(
            user=user,
            email=user.email,
            verified=True,
            primary=True
        )
        self.user = user
        self.token = token
        self.emailaddress = emailaddress
        self.login_url = api_reverse("api:auth:login")
        self.user_details_url = api_reverse("api:auth:user_details")
        self.register_url = api_reverse("api:auth:register")
        self.password_reset_url = api_reverse("api:auth:password_reset")
        self.password_change_url = api_reverse("api:auth:password_change")
        self.logout_url = api_reverse("api:auth:logout")

    def test_api_auth_login_success(self):
        """Test if valid credentials return token, name and uuid."""
        data = {"email": "testuser@test.com", "password": "test1234test"}
        response = self.client.post(self.login_url, data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.token.key)
        self.assertContains(response, self.user.name)
        self.assertContains(response, self.user.uuid)

    def test_api_auth_login_not_return_credentials_succes(self):
        """Test that correct login does not return email or password.
           We do not want to save login credentials anywhere."""
        data = {"email": "testuser@test.com", "password": "test1234test"}
        response = self.client.post(self.login_url, data)
        self.assertFalse(self.user.email in response.data)
        self.assertFalse(self.user.email in response.data.values())
        self.assertFalse("test1234test" in response.data)
        self.assertFalse("test1234test" in response.data.values())

    def test_api_auth_login_creates_token_success(self):
        """Test if a user without token gets a token by logging in."""
        tokens = Token.objects.all()
        tokencount = tokens.count()
        user = User.objects.create_user(
            email="newtestuser@test.com",
            password="test1234test"
        )
        emailaddress = EmailAddress.objects.get_or_create(
            user=user,
            email=user.email,
            verified=True,
            primary=True
        )
        data = {"email": "newtestuser@test.com", "password": "test1234test"}
        response = self.client.post(self.login_url, data)
        self.assertEqual(tokens.count(), tokencount + 1)

    def test_api_auth_login_wrong_password_fail(self):
        """Test if invalid password returns error."""
        data = {"email": "testuser@test.com", "password": "incorrectpassword"}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["non_field_errors"][0],
            "Unable to log in with provided credentials."
        )

    def test_api_auth_login_wrong_email_fail(self):
        """Test if invalid email returns error."""
        data = {"email": "wrongmail@test.com", "password": "test1234test"}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["non_field_errors"][0],
            "Unable to log in with provided credentials."
        )

    def test_api_auth_login_fields_required_fail(self):
        """Test if missing credentials returns field required error."""
        data = {}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRaises(serializers.ValidationError)
        self.assertTrue("This field is required." in response.data['password'])

    def test_api_auth_login_not_verified_fail(self):
        """Test if a user who is not verified is denied login."""
        data = {"email": "testuser@test.com", "password": "test1234test"}
        self.emailaddress[0].verified = False
        self.emailaddress[0].save()
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(
            "E-mail is not verified." in response.data["non_field_errors"]
        )

    def test_api_auth_password_reset_mail_send_success(self):
        """Test if a password reset email has been send."""
        data = {"email": "testuser@test.com"}
        response = self.client.post(self.password_reset_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        self.assertContains(response, "Password reset e-mail has been sent.")

    def test_api_auth_password_reset_mail_no_account_fail(self):
        """Test if no password reset email gets send for invalid email."""
        data = {"email": "nonexistentemail@test.com"}
        response = self.client.post(self.password_reset_url, data)
        self.assertEqual(len(mail.outbox), 0)

    def test_api_auth_register_success(self):
        """Test if valid credentials create user, which is unverified."""
        users = User.objects.all()
        usercount = users.count()
        data = {
            "email": "newtestuser@test.com",
            "password1": "test1234test",
            "password2": "test1234test"
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(users.count(), usercount + 1)
        emailaddress = EmailAddress.objects.get(email=data["email"])
        self.assertFalse(emailaddress.verified)

    def test_api_auth_register_email_send_success(self):
        """Test if valid credentials lead to sending of verification email."""
        data = {
            "email": "newtestuser@test.com",
            "password1": "test1234test",
            "password2": "test1234test"
        }
        response = self.client.post(self.register_url, data)
        content = {"detail": "Verification e-mail sent."}
        self.assertEqual(response.data, content)
        self.assertEqual(len(mail.outbox), 1)

    def test_api_auth_register_email_verification_success(self):
        """Test if visiting the verification mail's url verifies email."""
        data = {
            "email": "newtestuser@test.com",
            "password1": "test1234test",
            "password2": "test1234test"
        }
        response = self.client.post(self.register_url, data)
        self.client.get(mail.outbox[0].body[-117:-41])
        emailaddress = EmailAddress.objects.get(email=data["email"])
        self.assertTrue(emailaddress.verified)

    def test_api_auth_register_email_exists_fail(self):
        """Test if email duplicate returns email already exists error."""
        data = {
            "email": "testuser@test.com",
            "password1": "test1234test",
            "password2": "test1234test"
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["email"][0],
            "A user is already registered with this e-mail address."
        )

    def test_api_auth_register_password_too_short_fail(self):
        """Test if 11 character password is too short and returns error."""
        data = {
            "email": "newtestuser@test.com",
            "password1": "shortpasswo",
            "password2": "shortpasswo"
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["password1"][0],
            "This password is too short. It must contain at least 12 characters."
        )

    def test_api_auth_register_fields_required_fail(self):
        """Test if missing credentials result in field required error."""
        data = {}
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["email"][0], "This field is required.")
        self.assertEqual(
            response.data["password1"][0], "This field is required."
        )
        self.assertEqual(
            response.data["password2"][0], "This field is required."
        )

    def test_api_auth_password_change_success(self):
        """Test if user can change his password with valid credentials."""
        self.assertTrue(self.user.check_password("test1234test"))
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        data = {
            "old_password": "test1234test",
            "new_password1": "thisisanewpassword",
            "new_password2": "thisisanewpassword",
        }
        response = self.client.post(self.password_change_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "New password has been saved.")
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("thisisanewpassword"))

    def test_api_auth_password_change_no_token_header_fail(self):
        """Test if user can't change his password with invalid credentials."""
        data = {
            "old_password": "test1234test",
            "new_password1": "anewpassword",
            "new_password2": "anewpassword",
        }
        response = self.client.post(self.password_change_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["detail"],
            "Authentication credentials were not provided."
        )
        self.assertTrue(self.user.check_password("test1234test"))

    def test_api_auth_password_change_wrong_old_password_fail(self):
        """Test if user can't change his password with wrong old_password."""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        data = {
            "old_password": "nottheoldpassword",
            "new_password1": "thisisanewpassword",
            "new_password2": "thisisanewpassword",
        }
        response = self.client.post(self.password_change_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["old_password"][0], "Invalid password")

    def test_api_auth_password_change_wrong_old_password_fail(self):
        """Test if user can't change his password with a short password."""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        data = {
            "old_password": "test1234test",
            "new_password1": "shortpasswo",
            "new_password2": "shortpasswo",
        }
        response = self.client.post(self.password_change_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["new_password2"][0],
            "This password is too short. It must contain at least 12 characters."
        )

    def test_api_auth_password_change_password_mismatch_fail(self):
        """Test if user can't change new passwords don't match."""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        data = {
            "old_password": "test1234test",
            "new_password1": "thisisanewpassword",
            "new_password2": "thisisnotthesamenewpassword",
        }
        response = self.client.post(self.password_change_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["new_password2"][0],
            "The two password fields didn't match."
        )

    def test_api_auth_password_change_credentials_missing_fail(self):
        """Test if missing credentials result in field required error."""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        data = {}
        response = self.client.post(self.password_change_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["old_password"][0], "This field is required."
        )
        self.assertEqual(
            response.data["new_password1"][0], "This field is required."
        )
        self.assertEqual(
            response.data["new_password2"][0], "This field is required."
        )

    def test_api_auth_retrieve_user_details_success(self):
        """Test if user with valid credentials can retrieve his details."""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.get(self.user_details_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.user.name)
        self.assertContains(response, self.user.uuid)

    def test_api_auth_update_put_user_details_success(self):
        """Test if user with valid credentials can update put his details."""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        data = {"name": "Test Brownie User"}
        response = self.client.put(self.user_details_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, data["name"])
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, data["name"])

    def test_api_auth_update_patch_user_details_success(self):
        """Test if user with valid credentials can update patch his details."""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        data = {"name": "Test Brownie User"}
        response = self.client.patch(self.user_details_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, data["name"])
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, data["name"])

    def test_api_auth_no_credentials_fail(self):
        """Test if a user without credentials can't update anyone."""
        data = {"name": "Test Brownie User"}
        response = self.client.put(self.user_details_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["detail"],
            "Authentication credentials were not provided."
        )

    def test_api_auth_logout_success(self):
        """Test if a user can logout, meaning his token gets destroyed."""
        tokens = Token.objects.all()
        tokencount = tokens.count()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "Successfully logged out.")
        self.assertEqual(Token.objects.count(), tokencount - 1)

    def test_api_auth_logout_no_credentials_fail(self):
        """Test if a user can't log anyone out, without credentials."""
        tokens = Token.objects.all()
        tokencount = tokens.count()
        response = self.client.post(self.logout_url)
        self.assertEqual(Token.objects.count(), tokencount)


class AccountsSocialAPIViewsTestCase(APITestCase):

    def setUp(self):
        self.test_facebook = False
        self.access_token = ""
        if self.test_facebook:
            fb = SocialApp.objects.create(
                provider="facebook",
                name="Facebook",
                client_id=get_env_variable("FACEBOOK_CLIENT_ID"),
                secret=get_env_variable("FACEBOOK_SECRET_KEY"),
            )
            fb.sites.add(Site.objects.first())
            fb.save()
        self.name = "Lisa Albfagihchffe Schrockson"
        self.email = "phiwguyiua_1526539968@tfbnw.net"
        self.fb_login_url = api_reverse("api:auth:fb_login")
        self.fb_connect_url = api_reverse("api:auth:fb_connect")

    def test_api_auth_social_facebook_register(self):
        """Test if valid access_token creates a new user.
           If this test fails, you might need a new access_token."""
        if self.test_facebook:
            users = User.objects.all()
            usercount = users.count()
            data = {"access_token": self.access_token}
            response = self.client.post(self.fb_login_url, data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue("key" in response.data)
            self.assertTrue("name" in response.data["user"])
            self.assertTrue("uuid" in response.data["user"])
            self.assertEqual(users.count(), usercount + 1)

    def test_api_auth_social_facebook_connect(self):
        """Test if valid access_token can connect data to existing account."""
        if self.test_facebook:
            user = User.objects.create_user(
                email=self.email,
                name=self.name,
                password="test1234test"
            )
            token, created = Token.objects.get_or_create(user=user)
            emailaddress = EmailAddress.objects.get_or_create(
                user=user,
                email=user.email,
                verified=True,
                primary=True
            )
            self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
            data = {"access_token": self.access_token}
            response = self.client.post(self.fb_connect_url, data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(SocialAccount.objects.first().user, user)
