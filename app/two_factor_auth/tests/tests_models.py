from django.test import TestCase
from two_factor_auth.models import AntiFraud

class AntiFraudTestCase(TestCase):

    def setUp(self):
        AntiFraud.objects.create(
            phone_number="+5584998545520",
            last_status="pending",
            max_sequence_unapproved=3,
        )

    def test_reset_max_sequence_unapproved(self):
        antifraud = AntiFraud.objects.get(phone_number="+5584998545520")
        antifraud.last_status = "approved"
        antifraud.save()
        max_sequence_unapproved = AntiFraud.objects.get(
            phone_number="+5584998545520"
        ).max_sequence_unapproved
        self.assertEqual(max_sequence_unapproved, 0)