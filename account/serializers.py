from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()

class UserCreateSerializer(UserCreateSerializer):
    image_url = serializers.SerializerMethodField()
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password','contract_no','image_url')

    def get_image_url(self, obj):
        return obj.image.url if obj.image else None