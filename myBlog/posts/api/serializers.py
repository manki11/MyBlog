from rest_framework.serializers import ModelSerializer
from posts.models import Post

class PostListSerializer(ModelSerializer):
    class Meta:
        model= Post
        fields=[
            'id',
            'title',
            'slug',
            'body',
            'date'
        ]

class PostDetailSerializer(ModelSerializer):
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
            'publish',
            'read_time'
        ]
        depth = 1