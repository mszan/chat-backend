from django.core import serializers
from django.shortcuts import render

from chat.models import Message


def index(request):
    return render(request, 'chat/index.html')


def room(request, room_name):
    last_messages = serializers.serialize("json", Message.objects.all())

    return render(request, 'chat/room.html', {
        'last_messages': last_messages,
        'room_name': room_name
    })
