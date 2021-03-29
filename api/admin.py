from django.contrib import admin

from api.models import Message, Room, RoomInviteKey, CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Message)
admin.site.register(Room)
admin.site.register(RoomInviteKey)
