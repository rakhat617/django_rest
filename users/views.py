from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.exceptions import APIException, MethodNotAllowed, PermissionDenied
from rest_framework import status
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
)
from django.db.models.query import QuerySet
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

from users.serializers import UserModelSerializer, ChangePasswordSerializer, UserSerializer


class RegistrationViewSet(ViewSet):
    permission_classes = [AllowAny]

    @swagger_auto_schema(responses={403: "Method not allowed"})
    def list(self, request: Request) -> Response:
        # return Response(
        #     status=status.HTTP_405_METHOD_NOT_ALLOWED,
        #     data="Not implemented",
        # )
        raise MethodNotAllowed(method="list") 

    @swagger_auto_schema(request_body=UserModelSerializer, responses={201: "User successfully created", 400: "Error", 409: "Conflict"})
    def create(self, request: Request) -> Response:
        s = UserModelSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        try:
            User.objects.create_user(**s.validated_data)
            # User.objects.create(
            #     username=s.validated_data.get("username"),
            #     first_name=s.validated_data.get("first_name"),
            #     last_name=s.validated_data.get("last_name"),
            #     email=s.validated_data.get("email"),
            #     password=make_password(s.validated_data.get("password")),
            # )
            return Response(
                data={"message": "success"}, status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                data={"error": str(e)}, status=status.HTTP_409_CONFLICT
            )


class UserViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def check_user(request: Request, pk: int) -> User:
        user = get_object_or_404(User, pk=pk)
        if request.user.pk != user.pk:
            raise PermissionDenied(detail="no access")
        return user

    @swagger_auto_schema(responses={200: UserSerializer(many=True)})
    def list(self, request: Request) -> Response:
        queryset = User.objects.all()
        serializer = UserModelSerializer(queryset, many=True)
        # if not serializer.data:
        #     return Response(
        #         status=status.HTTP_404_NOT_FOUND,
        #         data={"error": "users not found"},
        #     )
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=None, responses={403: "Method not allowed"})
    def create(self, request: Request) -> Response:
        # return Response(
        #     status=status.HTTP_405_METHOD_NOT_ALLOWED,
        #     data="Not implemented"
        # )
        raise MethodNotAllowed(method="create") 
    
    @swagger_auto_schema(responses={200: UserSerializer, 404: "Not found"})
    def retrieve(self, request: Request, pk=None) -> Response:
        user = get_object_or_404(User, pk=pk)
        serializer = UserModelSerializer(user)
        return Response(data=serializer.data)
        # try:
        #     user = User.objects.get(pk=pk)
        #     serializer = UserModelSerializer(user)
        #     return Response(data=serializer.data)
        # except Exception as e:
        #     return Response(
        #         data={"error": str(e)}, 
        #         status=status.HTTP_404_NOT_FOUND
        #     )

    @swagger_auto_schema(request_body=UserModelSerializer, responses={200: "OK", 404: "Not found", 403: "Not allowed", 400: "Serializer error"})
    def update(self, request: Request, pk: int) -> Response:
        user = self.check_user(request=request, pk=pk)
        serializer = UserModelSerializer(
            instance=user, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={"message": "user updated"})

    @swagger_auto_schema(request_body=UserModelSerializer, responses={200: "OK", 404: "Not found", 403: "Not allowed", 400: "Serializer error"})
    def partial_update(self, request: Request, pk: int) -> Response:
        user = self.check_user(request=request, pk=pk)
        serializer = UserModelSerializer(
            instance=user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={"message": "user partial updated"})

    @swagger_auto_schema(request_body=UserModelSerializer, responses={200: "OK", 404: "Not found", 403: "Not allowed"})
    def destroy(self, request: Request, pk=None) -> Response:
        user = self.check_user(request=request, pk=pk)
        # user: User | None = User.objects.filter(pk=pk).first()
        # if not user:
        #     return Response(
        #         data={"error": "user not found"},
        #         status=status.HTTP_404_NOT_FOUND
        #     )
        # if request.user.pk != user.pk:
            # return Response(
            #     data={"message": "you have no power"},
            #     status=status.HTTP_400_BAD_REQUEST
            # )
        user.delete()
        return Response(
            data={"message": "user has been deleted"}
        )   


class ChangePasswordViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request: Request) -> Response:
        serializer = ChangePasswordSerializer(data=request.data, context={"request":request})
        user = request.user
        serializer.is_valid(raise_exception=True)
        user.password = make_password(password=serializer.validated_data["new_password"])
        user.save()
        return Response(data={"message": "Пароль успешно изменен"})


class UsersAllAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: UserModelSerializer(many=True)})
    def get(self, request):
        queryset = User.objects.all()
        serializer = UserModelSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=None, responses={403: "Method not allowed"})
    def post(self, request):
        raise MethodNotAllowed("POST")


class UserOneAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def check_user(request, user):
        if request.user.pk != user.pk:
            raise PermissionDenied("no access")
        return user

    @swagger_auto_schema(responses={200: UserModelSerializer, 404: "Not found"})
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserModelSerializer(user)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=UserModelSerializer, responses={200: "OK", 404: "Not found", 403: "Not allowed", 400: "Serializer error"})
    def put(self, request, pk):
        user = self.check_user(request, get_object_or_404(User, pk=pk))
        serializer = UserModelSerializer(instance=user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "user updated"})

    @swagger_auto_schema(request_body=UserModelSerializer, responses={200: "OK", 404: "Not found", 403: "Not allowed", 400: "Serializer error"})
    def patch(self, request, pk):
        user = self.check_user(request, get_object_or_404(User, pk=pk))
        serializer = UserModelSerializer(instance=user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "user partial updated"})

    @swagger_auto_schema(responses={200: "OK", 404: "Not found", 403: "Not allowed"})
    def delete(self, request, pk):
        user = self.check_user(request, get_object_or_404(User, pk=pk))
        user.delete()
        return Response({"message": "user has been deleted"})

