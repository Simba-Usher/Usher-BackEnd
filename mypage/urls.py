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
]
