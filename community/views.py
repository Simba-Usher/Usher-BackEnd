from django.shortcuts import render, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q

from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter


from .models import *
from .serializers import *
from .permissions import IsOwnerOrReadOnly
from .paginations import ComPostPagination

class ComPostFilter(filters.FilterSet):
    category = filters.ChoiceFilter(choices=ComPost.category_choices)
    
    class Meta:
        model = ComPost
        fields = ['category']

class ComPostViewSet(viewsets.ModelViewSet):
    queryset = ComPost.objects.annotate(
        like_cnt=Count(
            "reactions", filter=Q(reactions__reaction="like"), distinct=True
        ),

    )
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ComPostFilter

    filterset_fields = ["title"]
    search_fields = ["title"]
    #ordering_fields = ["-created_at"]
    pagination_class = ComPostPagination
    

    def get_permissions(self):
        if self.action in ["destroy"]:
            return [IsOwnerOrReadOnly()]
        elif self.action in ["create"]:
            return [IsAuthenticated()]
        return []
    
    def get_serializer_class(self):
        if self.action == "list":
            return ComPostListSerializer
        return ComPostSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data)

    @action(methods=["POST"], detail=True, permission_classes=[IsAuthenticated])
    def likes(self, request, pk=None):
        compost = self.get_object()
        user = request.user

        try:
            existing_reaction = CommunityReaction.objects.get(compost=compost, user=user, reaction="like")
            existing_reaction.delete()
            return Response({"detail": "좋아요 취소"}, status=status.HTTP_200_OK)
        except CommunityReaction.DoesNotExist:
            CommunityReaction.objects.create(compost=compost, user=user, reaction="like")
            return Response({"detail": "좋아요!"}, status=status.HTTP_201_CREATED)

    #실시간 인기글
    @action(detail=False, methods=["GET"])
    def hot(self, request):
        hot = self.queryset.filter(like_cnt__gte=10)
        page = self.paginate_queryset(hot)  
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)  
        
#게시글 댓글 많은 순
#    @action(detail=False, methods=["GET"])
#    def cmt(self, request):
#        composts = self.queryset.order_by("-comcomments_cnt")
#        page = self.paginate_queryset(composts)  # Apply pagination
#        serializer = self.get_serializer(page, many=True)
#        return self.get_paginated_response(serializer.data)  # Return paginated response

#게시글 좋아요 많은 순
#    @action(detail=False, methods=["GET"])
#    def popular(self, request):
#        composts = self.queryset.order_by("-like_cnt")
#        page = self.paginate_queryset(composts)  # Apply pagination
#        serializer = self.get_serializer(page, many=True)
#        return self.get_paginated_response(serializer.data)  # Return paginated response

#게시글 최근 순
#    @action(detail=False, methods=["GET"])
#    def recent(self, request):
#        composts = self.queryset.order_by("-created_at")
#        page = self.paginate_queryset(composts)  # Apply pagination
#        serializer = self.get_serializer(page, many=True)
#        return self.get_paginated_response(serializer.data)  # Return paginated response

#게시글 오래된 순 을 조회수 순으로 바꿔야 함
    #@action(detail=False, methods=["GET"])
    #def view(self, request):
        #composts = self.queryset.order_by("")
        #page = self.paginate_queryset(composts)  # Apply pagination
        #serializer = self.get_serializer(page, many=True)
        #return self.get_paginated_response(serializer.data)  # Return paginated response

#댓글 detail 뷰셋
class ComCommentViewSet(
    viewsets.GenericViewSet, 
    mixins.RetrieveModelMixin, 
    mixins.DestroyModelMixin,
    ):
    queryset = ComComment.objects.all()
    serializer_class = ComCommentSerializer

    def get_permissions(self):
        if self.action in ["create", "destroy"]:
            return [IsOwnerOrReadOnly()]
        return []

    def get_objects(self):
        obj = super().get_object()
        return obj

#댓글 작성 뷰셋 
class CommunityComCommentViewSet(
    viewsets.GenericViewSet, 
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    ):
    serializer_class = ComCommentSerializer
    #permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            return [IsAuthenticated()]
        return []

    def get_queryset(self):
        compost = self.kwargs.get("compost_id")
        queryset = ComComment.objects.filter(compost_id=compost)
        return queryset

    def create(self, request, compost_id=None):
        compost = get_object_or_404(ComPost, id=compost_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(compost=compost)
        return Response(serializer.data)

#대댓글 작성 관련 뷰셋
class CommunityComReplyViewSet(
    viewsets.GenericViewSet, 
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    ):
    queryset = ComReply.objects.all()
    serializer_class = ComReplySerializer


    # url 에서 comcomment_id 를 가져옴
    def get_queryset(self):
        comcomment = self.kwargs.get("comcomment_id")
        queryset = ComReply.objects.filter(comcomment_id=comcomment)
        return queryset
    
    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            return [IsAuthenticated()]
        return []
    
    def create(self, request, comcomment_id=None):
        comcomment = get_object_or_404(ComComment, id=comcomment_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(comcomment=comcomment)
        return Response(serializer.data)

# 대댓글 detail 관련 뷰셋
class ComReplyViewSet(
    viewsets.GenericViewSet, 
    mixins.DestroyModelMixin, 
    mixins.ListModelMixin, 
    mixins.RetrieveModelMixin
    ):
    queryset = ComReply.objects.all()
    serializer_class = ComReplySerializer

    # 읽기만 가능
    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            return [IsAuthenticated()]
        return []