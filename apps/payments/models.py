from django.db import models
from uuid import uuid4
from iamport import Iamport
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import Http404
from apps.songs.models import Song
import logging

User = get_user_model()

logger = logging.getLogger("portone")

class Payment(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uid = models.UUIDField(default=uuid4, editable=False)

    @property
    def merchant_uid(self):
        return self.uid

    song = models.ForeignKey(Song, on_delete=models.CASCADE)
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
    
    def get_status_display(self):
        status_display = {
            "ready": "미결제",
            "paid": "결제 완료",
            "cancelled": "결제 취소",
            "failed": "결제 실패"
        }
        return status_display.get(self.status)
    
    is_paid = models.BooleanField(default=False, db_index=True)
    
    def verify(self, commit=True):
        api = Iamport(imp_key=settings.PORTONE_API_KEY, imp_secret=settings.PORTONE_API_SECRET)
        
        try:
            meta = api.find(merchant_uid=self.merchant_uid)
        except (Iamport.ResponseError, Iamport.ResponseError) as e:
            logger.error(str(e), exc_info=e)
            raise Http404(str(e))
            

        self.status = meta['status']
        self.is_paid = meta['status'] == 'paid' and meta['amount'] == self.amount
        if commit:
            self.save()
        
        