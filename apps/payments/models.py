from django.db import models
from uuid import uuid4

# Create your models here.
class Payment(models.Model):
    
    uid = models.UUIDField(default=uuid4, editable=False)

    @property
    def merchant_uid(self):
        return self.uid

    name = models.CharField(max_length=255)
    amount = models.PositiveIntegerField()

    STATUS_CHOICES = (
        ("ready", "미결제"),
        ("paid", "결제 완료"),
        ("cancelled", "결제 취소"),
        ("failed", "결제 실패"),
    )

    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="ready", db_index=True
    )
    is_paid = models.BooleanField(default=False, db_index=True)