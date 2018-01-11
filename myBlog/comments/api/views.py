from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    DestroyAPIView,
    CreateAPIView
)

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly
)

from comments.models import Comment
from .serializers import CommentDetailSerializer

from posts.api.permissions import isOwnerorReadOnly


# class PostCreateAPIView(CreateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostCreateUpdateSerializer
#     permission_classes = [
#         IsAuthenticated
#     ]
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)


# class PostListAPIView(ListAPIView):
#     serializer_class = CommentSerializer
#     queryset = Comment.objects.all()

    # def get_queryset(self, *args, **kwargs):
    #     posts_list = Post.objects.all()
    #     query = self.request.GET.get("q")
    #     if query:
    #         posts_list = Post.objects.filter(
    #             Q(title__icontains=query) |
    #             Q(body__icontains=query) |
    #             Q(user__first_name__icontains=query) |
    #             Q(user__last_name__icontains=query)
    #         ).distinct()
    #     return posts_list


# class PostUpdateAPIView(RetrieveUpdateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostCreateUpdateSerializer
#     permission_classes = [isOwnerorReadOnly]


# class PostDeleteAPIView(DestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostDetailSerializer
#     permission_classes = [isOwnerorReadOnly]


class CommentDetailAPIView(RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentDetailSerializer