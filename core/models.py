from django.db import models

# Create your models here.


class TimeStampedModel(models.Model):

    """Time Stamped aasfa"""

    created = models.DateTimeField(auto_now_add=True)
    # auto_now : 모델을 저장할 때 date, time을 가져온다. > update
    # auto_now_add : 모델을 생성할 때마다 date, time을 가져온다. > create
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        # abstract model : 모델이지만 DB에는 나타나지 않는 모델
        # 확장하기 위해 사용 >> 다른 모델의 공통된 부분을 포함
