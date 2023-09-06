from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import *

app_name = "mypage"

router = SimpleRouter(trailing_slash=False)
router.register(r'memos', MemoViewSet, basename='memos')

urlpatterns = [
    path('mypage/', include(router.urls)),
    path('mypage/ticket', TicketView.as_view(), name='ticket'),
    path('mypage/profile', ProfileUpdateView.as_view(), name='profile_update'),
    path('mypage/liked-mainposts', LikedMainPostListView.as_view(), name='liked-mainposts'),
    path('mypage/liked-composts', LikedComPostListView.as_view(), name='liked-composts'),
    path('mypage/myreviews', MyMainReviewListView.as_view(), name='myreviews'),
    path('mypage/mycomposts', MyComPostListView.as_view(), name='mycomposts'),
]
