from rest_framework import serializers
from .models import *
from rest_framework.serializers import ListField

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username',]  

class ComPostSerializer(serializers.ModelSerializer):
    writer = CustomUserSerializer(read_only=True)
    #writer = serializers.CharField(source='writer.username', read_only=True)
    comcomments = serializers.SerializerMethodField()
    image = serializers.ImageField(use_url=True, required=False)
    like_cnt = serializers.SerializerMethodField()

    def get_like_cnt(self, instance):
        return instance.reactions.filter(reaction='like').count()

    def get_comcomments(self, instance):
        serializer = ComCommentSerializer(instance.comcomments, many=True)
        return serializer.data

    def create(self, validated_data):
        media_data = self.context['request'].FILES
        writer_id = self.context['request'].user.id  
        compost = ComPost.objects.create(writer_id=writer_id, **validated_data) 
        for media_data in media_data.getlist('media'):
            ComPostMedia.objects.create(compost=compost, media=media_data)
        return compost

    class Meta:
        model = ComPost
        fields = [
            'id',
            'title',
            'writer',
            'content',
            'created_at',
            'updated_at',
            'comcomments',
            'comcomments_cnt',
            'image',
            'like_cnt',
            'category',
        ]
        read_only_fields = ['id', 'writer', 'created_at', 'updated_at', 'comcomments', 'comcomments_cnt', 'like_cnt']

class ComPostListSerializer(serializers.ModelSerializer):
    writer = CustomUserSerializer(read_only=True)
    #writer = serializers.CharField(source='writer.username', read_only=True)
    comcomments_cnt = serializers.SerializerMethodField()
    like_cnt = serializers.SerializerMethodField()
    image = serializers.ImageField(use_url=True, required=False)

    def get_like_cnt(self, instance):
        return instance.reactions.filter(reaction='like').count()

    def get_comcomments_cnt(self, instance):
        return instance.comcomments.count()
        
    class Meta:
        model = ComPost
        fields = [
            'id',
            'title',
            'content',
            'created_at',
            'updated_at',
            'comcomments_cnt',
            'like_cnt',
            'image',
            'writer',
            'category',
        ]
        read_only_fields = ['category', 'id', 'writer', 'created_at', 'updated_at', 'comcomments_cnt', 'like_cnt']

class ComCommentSerializer(serializers.ModelSerializer):
    writer = CustomUserSerializer(read_only=True)
    #writer = serializers.CharField(source='writer.username', read_only=True)
    compost = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()

    def get_compost(self, instance):
        return instance.compost.title
    
    def get_replies(self, instance):
        serializers = ComReplySerializer(instance.comreplies.all(), many=True)
        return serializers.data

    class Meta:
        model = ComComment
        fields = '__all__'
        read_only_fields = ['compost', 'id', 'writer']

class ComReplySerializer(serializers.ModelSerializer):
    writer = CustomUserSerializer(read_only=True)
    comcomment = serializers.SerializerMethodField()
    #writer = serializers.CharField(source='writer.username', read_only=True)

    def get_comcomment(self, instance):
        return instance.comcomment.content

    class Meta:
        model = ComReply
        fields = [
            'id',
            'writer',
            'content',
            'created_at',
            'comcomment',
        ]
        read_only_fields = [
            'comcomment', 'writer'
        ]