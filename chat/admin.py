from django.contrib import admin

from chat.models import Message, Room, RoomInviteKey

admin.site.register(Message)
admin.site.register(Room)
admin.site.register(RoomInviteKey)
