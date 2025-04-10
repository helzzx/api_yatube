from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from django.urls import include, path
from api.views import PostViewSet, GroupViewSet, CommentViewSet
from rest_framework.authtoken import views


router = DefaultRouter()
router.register('posts', PostViewSet)
router.register('groups', GroupViewSet)

# Вложенный роутер для комментариев 
posts_router = routers.NestedSimpleRouter(router, 'posts', lookup='post')
posts_router.register('comments', CommentViewSet, basename='post-comments')

urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token),
    path('', include(router.urls)),
    path('', include(posts_router.urls)),
]
