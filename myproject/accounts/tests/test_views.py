from django.test import TestCase
from django.urls import reverse


class AccountsViewsTestCase(TestCase):

    def setUp(self):
        self.email_activation_done_url = reverse(
            'accounts:email_activation_done'
        )
        self.account_email_verification_sent_url = reverse(
            'accounts:account_email_verification_sent'
        )

    def test_email_activation_done(self):
        response = self.client.get(self.email_activation_done_url)
        self.assertContains(
            response,
            'Thank you for your email confirmation. You can now use your account.'
        )

    def test_account_email_verification_sent(self):
        response = self.client.get(self.account_email_verification_sent_url)
        self.assertContains(
            response,
            'Thank you for your registration. An email with an activation link has been send.'
        )
