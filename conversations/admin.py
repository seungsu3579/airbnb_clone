from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):

    """ Message Model Admin """

    list_display = ("__str__", "created",)

@admin.register(models.Conversation)
class ConversationAdmin(admin.ModelAdmin):

    """ Conversation Model Admin """

    filter_horizontal = (
        "participants",
    )

    list_display = ("__str__", "count_messages", "count_participants")

