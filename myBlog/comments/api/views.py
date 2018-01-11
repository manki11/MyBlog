from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    DestroyAPIView,
    CreateAPIView
)

from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin

from rest_framework.permissions import (
    IsAuthenticated,
)

from comments.models import Comment
from .serializers import CommentDetailSerializer, comment_create_serializer

from posts.api.permissions import isOwnerorReadOnly


class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    permission_classes = [
        IsAuthenticated
    ]

    def get_serializer_class(self):
        model_type= self.request.GET.get('type')
        id= self.request.GET.get('post_id')
        parent_id= self.request.GET.get('parent_id', None)
        return comment_create_serializer(
            model_type=model_type,
            id=id,
            parent_id=parent_id,
            user=self.request.user
        )


class CommentDetailAPIView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentDetailSerializer
    permission_classes = [isOwnerorReadOnly]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)