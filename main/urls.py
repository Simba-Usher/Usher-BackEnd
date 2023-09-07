from django.urls import path, include
from .views import *
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

app_name = "main"

router = routers.SimpleRouter(trailing_slash=False)

# MainPost related URLs
router.register("mainposts", MainPostViewSet, basename="mainposts")

# MainReview related URLs
router.register("mainposts/(?P<mainpost_id>\d+)/mainreviews", MainReviewWriteViewSet, basename="mainreview-write")
router.register("mainreviews", MainReviewViewSet, basename="mainreviews")

# MainReviewComment related URLs
router.register("mainreviews/(?P<mainreview_id>\d+)/mainrecoms", MainReviewCommentWriteViewSet, basename="mainrecom-write")
router.register("mainrecoms", MainReviewCommentViewSet, basename="mainrecoms")

urlpatterns = [
    path("", include(router.urls)),
]
