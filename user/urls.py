from dj_rest_auth.registration.views import VerifyEmailView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from django.urls import path, include, re_path
from .views import *

urlpatterns = [
    # 일반 회원 회원가입/로그인
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('dj-rest-auth/logout/', LogoutView.as_view(), name='rest_logout'),

    #토큰 관련
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # 유효한 이메일이 유저에게 전달
    re_path(r'^account-confirm-email/$', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    # 유저가 클릭한 이메일(=링크) 확인
    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$', ConfirmEmailView.as_view(), name='account_confirm_email'),
]
