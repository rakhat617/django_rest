from rest_framework import serializers

from chats.models import Chat, Message
from chats.utils import encrypt_message, decrypt_message
from users.serializers import UserSerializer


class ChatViewSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    is_group = serializers.BooleanField()
    title = serializers.CharField(max_length=100)
    users = UserSerializer(many=True)

class ChatSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    is_group = serializers.BooleanField()
    title = serializers.CharField(max_length=100)
    users = serializers.ListField(child=serializers.IntegerField())

    def create(self, validated_data: dict):
        chat = Chat(
            is_group=validated_data.get("is_group"),
            title=validated_data.get("title"),
        )
        chat.save()
        users = validated_data.get("users")
        chat.users.set(users)
        return chat

    def update(self, instance: Chat, validated_data: dict):
        users = validated_data.pop("users")
        if users:
            instance.users.set(users)
        return super().update(instance, validated_data)


class MessageViewSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    text = serializers.CharField(max_length=2000)
    chat = ChatViewSerializer()
    parent_message = serializers.PrimaryKeyRelatedField(queryset=Chat.objects.all())
    sender = UserSerializer()


class MessageSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    text = serializers.CharField(max_length=2000)
    chat = serializers.PrimaryKeyRelatedField(queryset=Chat.objects.all())
    parent_message = serializers.PrimaryKeyRelatedField(queryset=Message.objects.all())

    def create(self, validated_data: dict):
        sender = self.context.get('sender')
        validated_data["sender"] = sender
        validated_data["text"] = encrypt_message(text=validated_data.get("text"))
        message = Message(**validated_data)
        # message = Message(
        #     text=validated_data.get("text"),
        #     chat=validated_data.get("chat")
        # )
        # message.sender = sender
        # if validated_data.get("parent_message"):
        #     message.parent_message = validated_data.get("parent_message")
        message.save()
        return message

    def update(self, instance: Message, validated_data: dict):
        forbidden_fields = set(validated_data.keys()) - {'text'}
        if forbidden_fields:
            raise serializers.ValidationError(
                f"Cannot update fields: {', '.join(forbidden_fields)}"
            )
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance
