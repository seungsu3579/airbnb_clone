from django.db import models
from django.urls import reverse
from django_countries.fields import CountryField
from core import models as core_models

# Create your models here.


class AbstractItem(core_models.TimeStampedModel):

    """Abstract Item"""

    name = models.CharField(max_length=80)

    def save(self, *args, **kwargs):
        self.name = str.capitalize(self.name)
        super().save(*args, **kwargs) # Call the real save() method

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

class RoomType(AbstractItem):

    """RoomType Models Definition"""

    class Meta:
        verbose_name = "Room Type"
        ordering = ['created']

class Amenity(AbstractItem):

    """Amenity Models Definition"""

    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):

    """Facility Models Definition"""
 
    class Meta:
        verbose_name_plural = "Facilities"

 
class HouseRule(AbstractItem):

    """HouseRule Models Definition"""

    class Meta:
        verbose_name = "House Rule"




class Room(core_models.TimeStampedModel):

    """Room Model Definition"""

    name = models.CharField(max_length=140)
    # 입력 필수 사항이기에 null,blank는 설정하지 않음(false)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField()
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()  # 0~24시까지
    check_out = models.TimeField()  # 0~24시까지
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey("users.User", related_name="rooms",on_delete=models.CASCADE)
    room_type = models.ForeignKey("RoomType", related_name="rooms",on_delete=models.SET_NULL, null=True)
    amenities = models.ManyToManyField("Amenity", related_name="rooms", blank=True)
    facilities = models.ManyToManyField("Facility", related_name="rooms", blank=True)
    house_rules = models.ManyToManyField("HouseRule", related_name="rooms", blank=True)

    # __str__()함수로 객체를 보여주는데 우리는 room name으로 객체를 관리하겠다.
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.city = str.capitalize(self.city)
        super().save(*args, **kwargs) # Call the real save() method

    def get_absolute_url(self):
        return reverse("rooms:detail", kwargs={'pk':self.pk})

    def total_rating(self):
        all_reviews = self.reviews.all()
        review_list = []
        if len(all_reviews) > 0:
            for review in all_reviews:
                review_list.append(review.rating_average())
            return round(sum(review_list)/len(review_list), 2)
        return 0


class Photo(core_models.TimeStampedModel): 

    """Photo Model Definition"""

    caption = models.CharField(max_length=80)
    file = models.ImageField(upload_to="room_photos")
    room = models.ForeignKey("Room", related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption