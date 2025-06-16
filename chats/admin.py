from django.contrib import admin

from chats.models import Chat, Message


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    model = Chat
    list_display = ("title", "is_group")
    list_filter = ("title",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    model = Message
    list_display = ("sent_at", "sender", "chat")
    list_filter = ("sent_at",)
