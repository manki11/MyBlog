from rest_framework import serializers
from posts.models import Post
from comments.api.serializers import CommentDetailSerializer
from accounts.api.serializers import UserSerializer


class PostListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='posts-api:detail',
    )
    user = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'body',
            'date',
            'url',
            'user'
        ]
        depth=1

    def get_user(self, obj):
        return UserSerializer(obj.user).data


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'title',
            'body',
            'publish'
        ]


class PostDetailSerializer(serializers.ModelSerializer):
    html = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'slug',
            'image',
            'html',
            'date',
            'user',
            'draft',
            'read_time',
            'comments'
        ]
        depth = 1

    def get_html(self, obj):
        return obj.get_markdown()

    def get_user(self, obj):
        return UserSerializer(obj.user).data

    def get_comments(self, obj):
        if obj.comments:
            return CommentDetailSerializer(obj.comments, many=True).data
