from django.db import models
import uuid
from django.dispatch import receiver

from core.util import Validators


class AntiFraud(models.Model):
    """
        Model that is used to prevent a user from using brute force attacks on 
        the verification code.

        As referenced in the Twilio documentation correct codes have the status
        "approved" and incorrect codes have the status "pending".
    """
    STATUS_CHOICES = (
        ("approved", "approved"),
        ("pending", "pending"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    phone_number = models.CharField(validators=[Validators.phone_validator], max_length=17)
    last_status = models.CharField(choices=STATUS_CHOICES)
    max_sequence_unapproved = models.IntegerField(default=0)


@receiver(models.signals.pre_save, sender=AntiFraud)
def reset_max_sequence_unapproved(sender, instance, *args, **kwargs):
    """
    The post_save method to reset the max_sequence_unapproved field.
    If the current last_status is approved, then the max_sequence_unapproved field
    turns back to 0.
    """
    if instance.last_status == "approved":
        instance.max_sequence_unapproved = 0
       
