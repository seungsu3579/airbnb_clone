from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models
from rooms import models as room_models

class RoomInline(admin.StackedInline):

    model = room_models.Room


# Register your models here. 아래는 Decorator로 class위에 존재해야한다.
# admin.site.register(models.User, CustomUserAdmin) 과 같은 의미
@admin.register(models.User)
class CustomUserAdmin(UserAdmin):

    """Custom User Admin"""

    inlines = (
        RoomInline,
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "bio",
                    "birthdate",
                    "language",
                    "currency",
                    "superhost",
                )
            },
        ),
    )

    list_filter = UserAdmin.list_filter + (
        "superhost",
    )

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "language",
        "currency",
        "superhost",
        "is_staff",
        "is_superuser",
    )

    # list_display = ("username", "gender", "language", "currency", "superhost")
    # userpage에서 어떤 컬럼을 보여줄지 선택

    # list_filter = ("language", "currency", "superhost")
    # userpage에서 어떤 컬럼 값 별로 필터 생성

