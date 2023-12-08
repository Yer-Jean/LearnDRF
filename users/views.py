from rest_framework import generics

from users.models import User
from users.permissions import IsSelfProfile
from users.serializers import UserSerializer, RestrictedUserSerializer


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserRetrieveAPIView(generics.RetrieveAPIView):
    # serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_serializer_class(self):
        # Динамически выбираем сериалайзер
        if self.request.user == self.get_object():
            # Если пользователь просматривает свой профиль
            return UserSerializer
        else:
            # Если пользователь просматривает чужой профиль
            return RestrictedUserSerializer


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsSelfProfile]


class UserDestroyAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsSelfProfile]
