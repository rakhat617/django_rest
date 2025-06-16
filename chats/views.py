from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.exceptions import PermissionDenied, MethodNotAllowed
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db.models import QuerySet
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.authentication import JWTAuthentication

from chats.models import Chat, Message
from chats.serializers import ChatSerializer, ChatViewSerializer, MessageSerializer, MessageViewSerializer

class ChatsViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(responses={
        200: ChatViewSerializer(many=True)
    })
    def list(self, request: Request) -> Response:
        chats: QuerySet[Chat] = request.user.chat_users.all()
        serializer = ChatViewSerializer(instance=chats, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=ChatSerializer,
        responses={
            201: ChatSerializer,
            400: "bad request"
        }
    )
    def create(self, request: Request) -> Response:
        serializer = ChatSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data="created")

    @swagger_auto_schema(
        responses={
            200: ChatViewSerializer,
            404: "chat does not exist"
        }
    )
    def retrieve(self, request: Request, pk: int) -> Response:
        try:
            chat: Chat = request.user.chat_users.get(pk=pk)
        except Chat.DoesNotExist:
            return Response(
                data="chat does not exist",
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ChatViewSerializer(instance=chat)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=ChatSerializer,
        responses={
            200: "chat updated",
            404: "bad request"
        }
    )
    def update(self, request: Request, pk: int) -> Response:
        chat: Chat = get_object_or_404(Chat, pk=pk, users=request.user)
        serializer = ChatSerializer(instance=chat, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data="chat updated", status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=ChatSerializer,
        responses={
            200: "chat updated",
            404: "bad request"
        }
    )
    def partial_update(self, request: Request, pk: int) -> Response:
        chat: Chat = get_object_or_404(Chat, pk=pk, users=request.user)
        serializer = ChatSerializer(instance=chat, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data="chat updated", status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={
            200: "chat was removed",
            404: "chat not found"
        }
    )
    def destroy(self, request: Request, pk: int) -> Response:
        chat: Chat = get_object_or_404(Chat, pk=pk, users=request.user)
        chat.delete()
        return Response(data="chat was removed", status=status.HTTP_200_OK)


class MessagesViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(responses={
        200: MessageViewSerializer(many=True)
    })
    def list(self, request: Request) -> Response:
        messages: QuerySet[Message] = request.user.message_sender.all()
        serializer = MessageViewSerializer(instance=messages, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=MessageSerializer,
        responses={
            201: MessageSerializer,
            400: "bad request"
        }
    )
    def create(self, request: Request) -> Response:
        serializer = MessageSerializer(data=request.data, context={"sender": request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data="created")

    @swagger_auto_schema(
        responses={
            200: MessageViewSerializer,
            404: "message does not exist"
        }
    )
    def retrieve(self, request: Request, pk: int) -> Response:
        try:
            message: Message = request.user.message_sender.get(pk=pk)
        except Message.DoesNotExist:
            return Response(
                data="message does not exist",
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = MessageViewSerializer(instance=message)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={403: "Method not allowed"})
    def update(self, request: Request, pk: int) -> Response:
        raise MethodNotAllowed(method="list") 
    
    @swagger_auto_schema(
        request_body=MessageSerializer,
        responses={
            200: "message edited",
            404: "bad request"
        }
    )
    def partial_update(self, request: Request, pk: int) -> Response:
        message: Message = get_object_or_404(Message, pk=pk, sender=request.user)
        serializer = MessageSerializer(instance=message, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data="message edited", status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={
            200: "message was deleted",
            404: "message not found"
        }
    )
    def destroy(self, request: Request, pk: int) -> Response:
        message: Message = get_object_or_404(Message, pk=pk, sender=request.user)
        message.delete()
        return Response(data="message was removed", status=status.HTTP_200_OK)