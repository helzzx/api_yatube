from rest_framework import viewsets, permissions
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated

from posts.models import Post, Comment, Group
from .serializers import PostSerializer, CommentSerializer, GroupSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in (permissions.SAFE_METHODS, 'POST'):
            return True
        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs.get('post_pk')
        post = Post.objects.filter(pk=post_id).first()
        if not post:
            raise NotFound('Post not found')
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        post = Post.objects.get(pk=self.kwargs['post_pk'])
        serializer.save(author=self.request.user, post=post)
