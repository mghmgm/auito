from rest_framework import serializers
from .models import Post, Ad
from django.utils import timezone


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

    def validate_pub_date(self, value):
        if value > timezone.now():
            raise serializers.ValidationError(
                "Дата публикации не может быть в будущем."
            )
        return value


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = "__all__"

    def validate_pub_date(self, value):
        if value > timezone.now():
            raise serializers.ValidationError(
                "Дата публикации не может быть в будущем."
            )
        return value
