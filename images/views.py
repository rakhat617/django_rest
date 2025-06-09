from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, parsers
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from images.models import Images
from images.serializers import ImageSerializer

class UserImageAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    @swagger_auto_schema(
        operation_summary="Получить изображение текущего пользователя",
        responses={
            200: ImageSerializer(),
            404: "Изображение не найдено"
        }
    )
    def get(self, request):
        """Получить изображение текущего пользователя"""
        image = getattr(request.user, "user_images", None)
        if not image:
            return Response({"detail": "Изображение не найдено"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ImageSerializer(image)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Загрузить изображение для текущего пользователя (если не существует)",
        request_body=ImageSerializer,
        consumes=["multipart/form-data"],
        responses={
            201: ImageSerializer(),
            400: "Изображение уже существует или некорректный запрос"
        }
    )
    def post(self, request):
        """Загрузить изображение для текущего пользователя (если не существует)"""
        if hasattr(request.user, "user_images"):
            return Response({"detail": "Изображение уже существует"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Обновить изображение пользователя",
        request_body=ImageSerializer,
        consumes=["multipart/form-data"],
        responses={
            200: ImageSerializer(),
            400: "Некорректный запрос",
            404: "Изображение не найдено"
        }
    )
    def put(self, request):
        """Обновить изображение пользователя"""
        image = getattr(request.user, "user_images", None)
        if not image:
            return Response({"detail": "Изображение не найдено"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ImageSerializer(instance=image, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Обновить изображение пользователя",
        request_body=ImageSerializer,
        consumes=["multipart/form-data"],
        responses={
            200: ImageSerializer(),
            400: "Некорректный запрос",
            404: "Изображение не найдено"
        }
    )
    def patch(self, request):
        """Обновить изображение пользователя"""
        image = getattr(request.user, "user_images", None)
        if not image:
            return Response({"detail": "Изображение не найдено"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ImageSerializer(instance=image, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Удалить изображение текущего пользователя",
        responses={
            204: "Изображение удалено",
            404: "Изображение не найдено"
        }
    )
    def delete(self, request):
        """Удалить изображение текущего пользователя"""
        image = getattr(request.user, "user_images", None)
        if not image:
            return Response({"detail": "Изображение не найдено"}, status=status.HTTP_404_NOT_FOUND)
        image.delete()
        return Response({"detail": "Изображение удалено"}, status=status.HTTP_204_NO_CONTENT)
