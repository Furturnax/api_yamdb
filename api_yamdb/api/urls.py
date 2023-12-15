from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import (
    APIGetToken,
    APISignup,
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
    UserViewSet,
)

router_v1 = DefaultRouter()

router_v1.register(
    'users',
    UserViewSet,
    basename='users'
)
router_v1.register(
    'titles',
    TitleViewSet,
    basename='titles'
)
router_v1.register(
    'genres',
    GenreViewSet,
    basename='genres'
)
router_v1.register(
    'categories',
    CategoryViewSet,
    basename='categories'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

auth_patterns = [
    path('token/', APIGetToken.as_view(), name='get_token'),
    path('signup/', APISignup.as_view(), name='signup'),
]

v1_patterns = [
    path('', include(router_v1.urls)),
    path('auth/', include(auth_patterns)),
]

urlpatterns = [
    path('v1/', include(v1_patterns)),
]
