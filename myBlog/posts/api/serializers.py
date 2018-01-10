from rest_framework import serializers
from posts.models import Post

class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model= Post
        fields=[
            'id',
            'title',
            'slug',
            'body',
            'date'
        ]

class PostCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model= Post
        fields=[
            'title',
            'body',
            'publish'
        ]

class PostDetailSerializer(serializers.ModelSerializer):
    # comments = serializers.BooleanField(source='comments')
    class Meta:
        model= Post
        fields=[
            'id',
            'title',
            'slug',
            'image',
            'body',
            'date',
            'user',
            'draft',
            'read_time',
            # 'comments'
        ]
        depth = 1