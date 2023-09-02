from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer as DefaultLoginSerializer
from rest_framework import serializers

class CustomRegisterSerializer(RegisterSerializer):
    name = serializers.CharField(max_length=255, required=True)
    username = None  # username을 제거합니다.

    def get_cleaned_data(self):
        super().get_cleaned_data()
        return {
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'email': self.validated_data.get('email', ''),
            'username': self.validated_data.get('username', ''),
        }

#pw 관련 오류 수정
#로그인 api 시리얼라이저 작성 -> 유저네임 받는 거 없애야 함
