from django.urls import path, include
from .views import *
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

app_name = "main"

default_router = routers.SimpleRouter(trailing_slash=False)
default_router.register("mainposts", MainPostViewSet, basename="mainposts")

mainreview_router = routers.SimpleRouter(trailing_slash=False)
mainreview_router.register("mainreviews", MainReviewViewSet, basename="mainreviews")

mainreview_write_router = routers.SimpleRouter(trailing_slash=False)
mainreview_write_router.register("mainreviews", MainReviewWriteViewSet, basename="mainreviews")

mainreviewcomment_router = routers.SimpleRouter(trailing_slash=False)
mainreviewcomment_router.register("mainrecoms", MainReviewCommentViewSet, basename="mainrecoms")

mainreviewcomment_write_router = routers.SimpleRouter(trailing_slash=False)
mainreviewcomment_write_router.register("mainrecoms", MainReviewCommentWriteViewSet, basename="mainrecoms")

urlpatterns = [
    path("", include(default_router.urls)),
    path("", include(mainreview_router.urls)),
    path("", include(mainreviewcomment_router.urls)),
    path("mainposts/<int:mainpost_id>/", include(mainreview_write_router.urls)),
    path("mainreviews/<int:mainreview_id>/", include(mainreviewcomment_write_router.urls)),
]