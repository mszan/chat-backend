from django.contrib import admin

from chat.models import Message, Room, InvitationKey

admin.site.register(Message)
admin.site.register(Room)
admin.site.register(InvitationKey)
