from rest_framework import serializers
from comments.models import Comment
from accounts.api.serializers import UserSerializer


class CommentDetailSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id',
            'user',
            'content',
            'timestamp',
            'content_type',
            'object_id',
            'parent',
            'replies'
        ]
        depth = 1

    def get_replies(self, obj):
        if obj.is_parent:
            return CommentChildSerializer(obj.children(), many=True).data
        return None

    def get_user(self, obj):
        return UserSerializer(obj.user).data


class CommentChildSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = [
            'id',
            'user',
            'content',
            'timestamp',
        ]
        depth = 1

    def get_user(self, obj):
        return UserSerializer(obj.user).data
