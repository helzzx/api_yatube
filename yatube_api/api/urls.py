from rest_framework.routers import DefaultRouter
from drf_nested_routers.routers import NestedSimpleRouter
from django.urls import include, path
from api.views import PostViewSet, GroupViewSet, CommentViewSet
from rest_framework.authtoken import views


router = DefaultRouter()
router.register('posts', PostViewSet)
router.register('groups', GroupViewSet)


posts_router = NestedSimpleRouter(router, 'posts', lookup='post')
posts_router.register('comments', CommentViewSet, basename='post-comments')

urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token),
    path('', include(router.urls)),
    path('', include(posts_router.urls)),
]
