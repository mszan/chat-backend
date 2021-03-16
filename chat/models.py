from django.db import models


class Message(models.Model):
    """
    Message model.
    """
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.TextField(null=False)

    def __str__(self):
        return f'Message {self.id}'
