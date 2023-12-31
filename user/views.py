from django.http import HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC
from rest_framework.response import Response

from rest_framework import viewsets, permissions
from .models import CustomUser
from .serializers import *
from rest_framework_simplejwt.views import TokenObtainPairView
from dj_rest_auth.views import LogoutView


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]
    

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            user_data = response.data.get('user', {})
            nickname = user_data.get('nickname', None)
            email = user_data.get('email', None)
            if nickname:
                response.data.update({"nickname": nickname})
            if email:
                response.data.update({"email": email})
            del response.data['user']  # user 객체는 응답에서 제거
        return response


class ConfirmEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, *args, **kwargs):
        self.object = confirmation = self.get_object()

        if confirmation:
            confirmation.confirm(self.request)
            
            return HttpResponseRedirect('http://welcometousher.site/success')
        else:
            return Response({"status": "failure", "message": "이메일 인증이 완료되었습니다."})

    def get_object(self, queryset=None):
        key = self.kwargs['key']
        email_confirmation = EmailConfirmationHMAC.from_key(key)
        if not email_confirmation:
            if queryset is None:
                queryset = self.get_queryset()
            try:
                email_confirmation = queryset.get(key=key.lower())
            except EmailConfirmation.DoesNotExist:
                return None
        return email_confirmation

    def get_queryset(self):
        qs = EmailConfirmation.objects.all_valid()
        qs = qs.select_related("email_address__user")
        return qs

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]  

    def get_serializer_context(self):
        # serializer의 context에 request 객체를 추가
        return {'request': self.request}

    def perform_update(self, serializer):
        # 업데이트를 수행할 때 admin만 grade를 수정할 수 있게 하는 추가 로직
        if 'grade' in serializer.validated_data and not self.request.user.is_staff:
            raise serializers.ValidationError({"grade": "Only admin can change the grade."})
        serializer.save()
    #validate data를 return 해가야 함
#        return Response(validate.)