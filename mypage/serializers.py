from rest_framework import serializers
from .models import *

from main.models import *
from community.models import *
from main.serializers import *
from community.serializers import *
from user.models import *
from user.backends import *

from dj_rest_auth.serializers import UserDetailsSerializer
from django.contrib.auth import get_user_model


class ProfileUpdateSerializer(UserDetailsSerializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, required=False)
    new_password_confirm = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = ['grade', 'email', 'nickname', 'old_password', 'new_password', 'new_password_confirm']
        read_only_fields = ['grade', 'email']

    def validate(self, data):
        new_password = data.get('new_password')
        new_password_confirm = data.get('new_password_confirm')
        old_password = data.get('old_password') 

        if new_password or new_password_confirm:
            if not old_password:
                raise serializers.ValidationError("기존 비밀번호를 입력해주세요.")
            if not self.instance.check_password(old_password):
                raise serializers.ValidationError("기존 비밀번호가 일치하지 않습니다.")
            if new_password != new_password_confirm:
                raise serializers.ValidationError("새 비밀번호와 새 비밀번호 확인이 일치하지 않습니다.")
        return data

    def validate_nickname(self, value):
        """ Check that nickname is unique. """
        if get_user_model().objects.exclude(pk=self.instance.pk).filter(nickname=value).exists():
            raise serializers.ValidationError("이미 사용 중인 닉네임입니다.")
        return value

    def update(self, instance, validated_data):
        if 'new_password' in validated_data:
            instance.set_password(validated_data['new_password'])
            validated_data.pop('new_password')
        validated_data.pop('old_password', None)
        validated_data.pop('new_password_confirm', None)
        
        # 닉네임 변경 로직
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.save()

        return super(ProfileUpdateSerializer, self).update(instance, validated_data)

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
            model = Ticket
            fields =  ['id', 'ticket_memo', 'ticket_number', 'performance', 'performance_location', 
            'performance_date', 'reservation_site', 'discount_method', 'price']
            read_only_fields = ['id', 'performance', 'performance_location', 
            'performance_date', 'reservation_site', 'discount_method', 'price']

#main앱에서 티켓 값 불러올 때 사용하는 시리얼라이저
class TicketReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['performance_date', 'reservation_site', 'discount_method', 'price']
        read_only_fields = ['performance_date', 'reservation_site', 'discount_method', 'price']

class MemoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Memo
        fields = ('id', 'title', 'date', 'location', 'content')
        read_only_fields = ['id']

    def create(self, validated_data):
        return Memo.objects.create(**validated_data)

