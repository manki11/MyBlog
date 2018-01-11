from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from comments.models import Comment
from accounts.api.serializers import UserSerializer
from rest_framework.exceptions import ValidationError

User = get_user_model()


def comment_create_serializer(model_type='post', id=None, parent_id=None, user=None):
    class CommentCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = Comment
            fields = [
                'id',
                'parent',
                'content',
                'timestamp'
            ]

        def __init__(self, *args, **kwargs):
            self.model_type = model_type
            self.id = id
            self.parent_obj = None
            if parent_id:
                parent_qs = Comment.objects.filter(id=parent_id)
                if parent_qs.exists() and parent_qs.count() == 1:
                    self.parent_obj = parent_qs.first()
            return super(CommentCreateSerializer, self).__init__(*args, **kwargs)

        def validate(self, data):
            model_type = self.model_type
            model_qs = ContentType.objects.filter(model=model_type)
            if not model_qs.exists() or model_qs.count() != 1:
                raise ValidationError("This is not a valid content-type")
            SomeModel = model_qs.first().model_class()
            obj_qs = SomeModel.objects.filter(id=id)
            if not obj_qs.exists() or obj_qs.count() != 1:
                raise ValidationError("This is not a valid id for content-type")
            return data

        def create(self, validated_data):
            content = validated_data.get('content')
            if not user:
                main_user = User.objects.all().first()
            else:
                main_user = user
            model_type = self.model_type
            id = self.id
            parent_obj = self.parent_obj
            comment = Comment.objects.create_by_model_type(
                model_type=model_type,
                user=main_user,
                id=id,
                parent_obj=parent_obj,
                content=content
            )
            return comment

    return CommentCreateSerializer


class CommentDetailSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    content_obj_url= serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id',
            'user',
            'content',
            'timestamp',
            'content_obj_url',
            'parent',
            'replies'
        ]
        depth = 1
        read_only_fields=[
            'id',
            'user',
            'parent',
            'replies'
        ]

    def get_replies(self, obj):
        if obj.is_parent:
            return CommentChildSerializer(obj.children(), many=True).data
        return None

    def get_content_obj_url(self, obj):
        return obj.content_object.get_api_path()

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
