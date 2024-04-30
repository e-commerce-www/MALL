from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Seller(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(
        max_length=11,  # 하이픈 없이 숫자만 저장하므로 길이를 11로 설정
        validators=[
            RegexValidator(
                regex=r'^01[016789][0-9]{8}$',  # 하이픈 없이 숫자만 받는 정규 표현식
                message="전화번호는 '01012345678' 형식이어야 합니다."
            )
        ],
    )
    
    def __str__(self):
        return self.user.username