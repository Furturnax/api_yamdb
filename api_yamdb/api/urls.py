from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import (
    # UserViewSet,
    # TitleViewSet,
    GenreViewSet,
    CategoryViewSet,
    # CommentViewSet,
    # ReviewViewSet,
    # APIGetToken,
    # APISignup
)


router_v1 = DefaultRouter()

# router_v1.register(
#     'users',
#     UserViewSet,
#     basename='users'
# )
# router_v1.register(
#     'titles',
#     TitleViewSet,
#     basename='titles'
# )
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
# router_v1.register(
#     r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
#     CommentViewSet,
#     basename='comments'
# )
# router_v1.register(
#     r'titles/(?P<title_id>\d+)/reviews',
#     ReviewViewSet,
#     basename='reviews'
# )

v1_patterns = [
    path('', include(router_v1.urls)),
#     path('auth/token/', APIGetToken.as_view(), name='get_token'),
#     path('auth/signup/', APISignup.as_view(), name='signup'),
]

urlpatterns = [
    path('v1/', include(v1_patterns)),
]
