from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer as DefaultLoginSerializer
from rest_framework import serializers
from .models import CustomUser

class CustomRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField(max_length=6, required=True) 

    def get_cleaned_data(self):
        cleaned_data = super().get_cleaned_data()
        cleaned_data.update({
            'nickname': self.validated_data.get('nickname', ''),
        })
        return cleaned_data

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # request 객체를 context에서 가져옴
        request = self.context.get('request', None)
        
        # 만약 request 객체가 있고, 사용자가 staff나 admin이 아니라면 grade 필드를 읽기 전용으로 설정
        if request and not request.user.is_staff:
            self.fields['grade'].read_only = True
