from django.db import models

from django.contrib.auth.models import User


class Chat(models.Model):
    is_group = models.BooleanField(
        verbose_name="групповой чат",
        default=False
    )
    title = models.CharField(
        verbose_name="название чата",
        max_length=100,
        blank=True
    )
    users = models.ManyToManyField(
        to=User,
        related_name="chat_users",
        verbose_name="участники чата"
    )

    class Meta:
        ordering=("id",)
        verbose_name = "чат"
        verbose_name_plural = "чаты"

    def __str__(self):
        return f"{self.pk} -> {self.is_group}"

class Message(models.Model):
    text = models.TextField(
        verbose_name="текст",
        max_length=2000,
        blank=True
    )
    sender = models.ForeignKey(
        to=User,
        verbose_name="отправитель",
        on_delete=models.SET_DEFAULT,
        default="anonymous",
        related_name="message_sender"
    )
    chat = models.ForeignKey(
        to=Chat,
        verbose_name="чат",
        on_delete=models.CASCADE,
        related_name="messages_chat"
    )
    sent_at = models.DateTimeField(
        verbose_name="дата отправки",
        auto_now_add=True
    )
    parent_message = models.ForeignKey(
        to="self",
        on_delete=models.SET_NULL,
        verbose_name="ответ на сообщение",
        related_name="message_parent",
        null=True
    )

    class Meta:
        ordering=("id",)
        verbose_name = "сообщение"
        verbose_name_plural = "сообщения"

    def __str__(self):
        return f"{self.text[:20]} | {self.sent_at} | {self.chat} | {self.sender}"