from django.urls import path, include, re_path
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
    re_path(r'^mainposts/(?P<mainpost_id>\d+)/mainreviews/latest', MainReviewViewSet.as_view({'get': 'latest'}), name='mainreview-latest'),
    re_path(r'^mainposts/(?P<mainpost_id>\d+)/mainreviews/popular', MainReviewViewSet.as_view({'get': 'popular'}), name='mainreview-popular'),
    re_path(r'^mainposts/(?P<mainpost_id>\d+)/mainreviews/(?P<pk>\d+)/likes/$', MainReviewViewSet.as_view({'post': 'likes'}), name='mainreview-likes-under-mainpost'),
]
