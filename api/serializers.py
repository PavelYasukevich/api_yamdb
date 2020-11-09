from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "bio", "email", "role"]


class MyTokenObtainPairSerializer(serializers.Serializer):
    email = serializers.EmailField()
    confirmation_code = serializers.CharField(max_length=255)

    def validate(self, data):
        user = get_object_or_404(
            User, email=data["email"], password=data["confirmation_code"]
        )

        refresh = RefreshToken.for_user(user)

        return {
            "access": str(refresh.access_token),
        }
