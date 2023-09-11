from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import *

app_name = "mypage"

router = SimpleRouter(trailing_slash=False)
router.register(r'memos', MemoViewSet, basename='memos')

urlpatterns = [
    path('mypage/', include(router.urls)),
    path('mypage/ticket', TicketView.as_view(), name='ticket'),
    path('mypage/ticket/<int:ticket_id>', TicketView.as_view(), name='ticket_detail'),
    path('mypage/profile', ProfileUpdateView.as_view(), name='profile_update'),
    path('mypage/liked-mainposts', LikedMainPostListView.as_view(), name='liked-mainposts'),
    path('mypage/liked-composts', LikedComPostListView.as_view(), name='liked-composts'),
    path('mypage/myreviews', MyMainReviewListView.as_view(), name='myreviews'),
    path('mypage/mycomposts', MyComPostListView.as_view(), name='mycomposts'),
    path('mypage/ticket/<int:ticket_id>/memo', TicketMemoView.as_view(), name='ticket_memo'),
]
