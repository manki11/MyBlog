from rest_framework import serializers
from posts.models import Post

class PostListSerializer(serializers.ModelSerializer):
    url= serializers.HyperlinkedIdentityField(
        view_name='posts-api:detail',
    )
    class Meta:
        model= Post
        fields=[
            'id',
            'title',
            'body',
            'date',
            'url'
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
    html= serializers.SerializerMethodField()

    class Meta:
        model= Post
        fields=[
            'id',
            'title',
            'slug',
            'image',
            'html',
            'date',
            'user',
            'draft',
            'read_time',
            # 'comments'
        ]
        depth = 1

    def get_html(self, obj):
        return obj.get_markdown()