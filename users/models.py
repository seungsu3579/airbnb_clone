from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class User(AbstractUser):
    """Custom User Mode"""

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"
    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )

    LANGUAGE_ENGLISH = "en"
    LANGUAGE_KOREAN = "ko"
    LANGUAGE_CHOICES = ((LANGUAGE_ENGLISH, "English"), (LANGUAGE_KOREAN, "Korean"))
    #                           DB용        form용

    CURRENCY_USD = "usd"
    CURRENCY_KR = "krw"
    CURRENCY_CHOICES = ((CURRENCY_USD, "USD"), (CURRENCY_KR, "KRW"))

    avatar = models.ImageField(upload_to="avatars", blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, blank=True)
    # charfield 는 한줄이며 글자수 제한이 있음
    # choices 속성으로 입력값을 제한할 수도 있다. (제한값은 튜플로 제공)
    # 이때는 MIGRATE할 필요가 없다. 왜냐면 FORM의 변화만 있었을 뿐 DB상의 변화는 없기 때문
    bio = models.TextField(blank=True)
    # textfield는 여러줄을 쓸수 있고 글자수 제한이 없음
    birthdate = models.DateField(blank=True, null=True)
    language = models.CharField(choices=LANGUAGE_CHOICES, max_length=2, blank=True)
    currency = models.CharField(choices=CURRENCY_CHOICES, max_length=3, blank=True)
    superhost = models.BooleanField(default=False)
