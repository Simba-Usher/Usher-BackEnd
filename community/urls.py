from django.urls import path, include
from .views import *
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

app_name = "community"

default_router = routers.SimpleRouter(trailing_slash=False)
default_router.register("composts", ComPostViewSet, basename="composts")

comcomment_router = routers.SimpleRouter(trailing_slash=False)
comcomment_router.register("comcomments", ComCommentViewSet, basename="comcomments")

community_comcomment_router = routers.SimpleRouter(trailing_slash=False)
community_comcomment_router.register("comcomments", CommunityComCommentViewSet, basename="comcomments")

comreply_router = routers.SimpleRouter(trailing_slash=False)
comreply_router.register("comreplies", ComReplyViewSet, basename="comreplies")

community_comreply_router = routers.SimpleRouter(trailing_slash=False)
community_comreply_router.register("comreplies", CommunityComReplyViewSet, basename="comreplies")

urlpatterns = [
    path("", include(default_router.urls)),
    path("", include(comcomment_router.urls)),
    path("", include(comreply_router.urls)),
    path("composts/<int:compost_id>/", include(community_comcomment_router.urls)),
    path("comcomments/<int:comcomment_id>/", include(community_comreply_router.urls)),
]