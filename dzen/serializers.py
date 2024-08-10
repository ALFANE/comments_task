from rest_framework import serializers

from dzen.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "username",
            "email",
            "home_page",
            "message",
            "main_comment",
            "created_at",
            "updated_at",
        ]
