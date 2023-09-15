from rest_framework import serializers
from .models import *
from rest_framework.serializers import ListField
from django.db.models import Avg

from mypage.models import Ticket
from mypage.serializers import TicketReviewSerializer

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['nickname']  

class MainPostSerializer(serializers.ModelSerializer):
    #writer = serializers.CharField(source='writer.nickname', read_only=True)
    mainreviews = serializers.SerializerMethodField()
    image = serializers.ImageField(use_url=True, required=False)
    like_cnt = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    def get_like_cnt(self, instance):
        return instance.reactions.filter(reaction='like').count()

    def get_mainreviews(self, instance):
        serializer = MainReviewSerializer(instance.mainreviews, many=True)
        return serializer.data

    def create(self, validated_data):
        media_data = self.context['request'].FILES
        writer_id = self.context['request'].user.id  
        mainpost = MainPost.objects.create(writer_id=writer_id, **validated_data) 
        for media_data in media_data.getlist('media'):
            MainPostMedia.objects.create(mainpost=mainpost, media=media_data)
        return mainpost

    #전체 별점 평균값 리턴 로직
    def get_average_rating(self, obj):
        return obj.mainreviews.aggregate(Avg('rating'))['rating__avg']

    class Meta:
        model = MainPost
        fields = [
            'id',
            'title',
            'content',
            'mainreviews',
            'mainreviews_cnt',
            'image',
            'like_cnt',
            'genre',
            'location',
            'average_rating',
            'reactions',
            'price',
            'start_date',
            'end_date',
            'sentence',
            'place',
        ]
        read_only_fields = ['id', 'mainreviews', 'mainreviews_cnt', 'like_cnt', 'average_rating',]

class MainPostListSerializer(serializers.ModelSerializer):
    #writer = CustomUserSerializer(read_only=True)
    #writer = serializers.CharField(source='writer.username', read_only=True)
    mainreviews_cnt = serializers.SerializerMethodField()
    like_cnt = serializers.SerializerMethodField()
    image = serializers.ImageField(use_url=True, required=False)
    is_liked = serializers.SerializerMethodField()

    def get_like_cnt(self, instance):
        return instance.reactions.filter(reaction='like').count()

    def get_mainreviews_cnt(self, instance):
        return instance.mainreviews.count()
    
    def get_average_rating(self, obj):
        avg_rating = obj.mainreviews.aggregate(Avg('rating'))['rating__avg']
        return avg_rating if avg_rating is not None else 0.0

    def get_is_liked(self, obj):
        user = self.context.get("user", None)
        if user and user.is_authenticated:
            return obj.liked_users.filter(id=user.id).exists()
        return False

        
    class Meta:
        model = MainPost
        fields = [
            'id',
            'title',
            'content',
            'mainreviews_cnt',
            'image',
            'like_cnt',
            'genre',
            'location',
            'start_date',
            'end_date',
            'sentence',
            'place',
            'is_liked'
        ]
        read_only_fields = ['id', 'like_cnt', 'writer', 'mainreviews_cnt', 'like_cnt', 'start_date', 'end_date', 'sentence', 'is_liked']

class MainReviewSerializer(serializers.ModelSerializer):
    #writer = CustomUserSerializer(source='writer.nickname', read_only=True)
    writer = serializers.CharField(source='writer.nickname', read_only=True)
    like_cnt = serializers.SerializerMethodField()
    mainpost = serializers.SerializerMethodField()
    mainrecoms = serializers.SerializerMethodField()
    mainrecoms_cnt = serializers.SerializerMethodField()
    ticket = TicketReviewSerializer(read_only=True)
    
    def get_like_cnt(self, instance):
        return instance.reactions.filter(reaction='like').count()

    def get_ticket(self, obj):
        return serializers.PrimaryKeyRelatedField(queryset=Ticket.objects.filter(writer=self.context['request'].user))

    def get_mainpost(self, instance):
        return instance.mainpost.title
    
    def get_mainrecoms(self, instance):
        serializers = MainReviewCommentSerializer(instance.mainrecoms.all(), many=True)
        return serializers.data
    
    def get_mainrecoms_cnt(self, obj):
        return obj.mainrecoms.count()

    class Meta:
        model = MainReview
        fields = '__all__'
        read_only_fields = ['id', 'writer', 'ticket', 'created_at', 'updated_at', 'mainrecoms', 'mainrecoms_cnt', 'like_cnt']

class MainReviewListSerializer(serializers.ModelSerializer):
    writer = serializers.CharField(source='writer.nickname', read_only=True)
    mainpost = serializers.SerializerMethodField()
    mainrecoms_cnt = serializers.SerializerMethodField()
    ticket = TicketReviewSerializer(read_only=True)  # 티켓의 세부 정보도 표시
    like_cnt = serializers.SerializerMethodField()

    def get_like_cnt(self, instance):
        return instance.reactions.filter(reaction='like').count()

    def get_mainpost(self, instance):
        return instance.mainpost.title
    
    def get_mainrecoms_cnt(self, obj):
        return obj.mainrecoms.count()

    class Meta:
        model = MainReview
        fields = [
            'id',
            'writer',
            'content',
            'rating',
            'mainrecoms_cnt',
            'ticket',
            'created_at',
            'updated_at',
            'like_cnt',
        ]
        read_only_fields = [
            'id', 'writer',  'ticket', 'created_at', 'updated_at', 'mainrecoms_cnt', 'like_cnt',
        ]

class MainReviewCommentSerializer(serializers.ModelSerializer):
    mainreview = serializers.SerializerMethodField()
    writer = serializers.CharField(source='writer.nickname', read_only=True)

    def get_mainreview(self, instance):
        return instance.mainreview.content

    class Meta:
        model = MainReviewComment
        fields = [
            'id',
            'writer',
            'content',
            'created_at',
            'mainreview',
        ]
        read_only_fields = [
            'id', 'mainreview', 'writer', 'created_at'
        ]