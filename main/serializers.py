from rest_framework import serializers
from .models import *
from rest_framework.serializers import ListField
from django.db.models import Avg

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username',]  

class MainPostSerializer(serializers.ModelSerializer):
    #writer = CustomUserSerializer(read_only=True)
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
        ]
        read_only_fields = ['id', 'writer', 'mainreviews', 'mainreviews_cnt', 'like_cnt', 'average_rating',]

class MainPostListSerializer(serializers.ModelSerializer):
    #writer = CustomUserSerializer(read_only=True)
    #writer = serializers.CharField(source='writer.username', read_only=True)
    mainreviews_cnt = serializers.SerializerMethodField()
    like_cnt = serializers.SerializerMethodField()
    image = serializers.ImageField(use_url=True, required=False)

    def get_like_cnt(self, instance):
        return instance.reactions.filter(reaction='like').count()

    def get_mainreviews_cnt(self, instance):
        return instance.mainreviews.count()
        
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
            'location'
        ]
        read_only_fields = ['id', 'writer', 'mainreviews', 'mainreviews_cnt', 'like_cnt']

class MainReviewSerializer(serializers.ModelSerializer):
    writer = CustomUserSerializer(read_only=True)
    #writer = serializers.CharField(source='writer.username', read_only=True)
    mainpost = serializers.SerializerMethodField()
    mainrecoms = serializers.SerializerMethodField()
    mainrecoms_cnt = serializers.SerializerMethodField()

    def get_mainpost(self, instance):
        return instance.mainpost.title
    
    def get_mainrecoms(self, instance):
        serializers = MainReComsSerializer(instance.mainrecoms.all(), many=True)
        return serializers.data

    class Meta:
        model = MainReview
        fields = '__all__'
        read_only_fields = ['mainpost', 'id', 'writer', 'ticket', 'created_at', 'updated_at', 'mainrecoms', 'mainrecoms_cnt']

class MainReviewCommentSerializer(serializers.ModelSerializer):
    writer = CustomUserSerializer(read_only=True)
    mainreview = serializers.SerializerMethodField()
    #writer = serializers.CharField(source='writer.username', read_only=True)

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
            'mainreview', 'writer', 'created_at'
        ]