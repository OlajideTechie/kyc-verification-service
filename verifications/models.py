import uuid
from django.db import models

"""Models for passport verification."""
class PassportVerification(models.Model):
    STATUS_SUBMITTED = "submitted"
    STATUS_PROCESSING = "processing"
    STATUS_VERIFIED = "verified"
    STATUS_FAILED = "failed"
    STATUS_REQUIRES_ACTION = "requires_action"
    STATUS_EXPIRED = "expired"

    STATUS_CHOICES = [
        (STATUS_SUBMITTED, "Submitted"),
        (STATUS_PROCESSING, "Processing"),
        (STATUS_VERIFIED, "Verified"),
        (STATUS_FAILED, "Failed"),
        (STATUS_REQUIRES_ACTION, "Requires Action"),
        (STATUS_EXPIRED, "Expired"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    passport_number = models.CharField(max_length=20)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_SUBMITTED
    )
    provider_reference = models.CharField(
        max_length=100, blank=True, null=True
    )

    provider_response = models.JSONField(
        null=True,
        blank=True,
        help_text="Raw response from Interswitch for audit/debugging",
    )

    failure_reason = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.passport_number} - {self.status}"