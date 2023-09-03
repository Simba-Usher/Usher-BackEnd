from django.shortcuts import render

from django.shortcuts import render, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q, Avg

from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter

from django_filters import DateFromToRangeFilter, Filter

from .models import *
from .serializers import *
from .permissions import IsOwnerOrReadOnly

def validate_thousand(value):
    if value % 1000 != 0:
        raise serializers.ValidationError("가격은 1000원 단위로 설정해야 합니다.")

class ThousandFilter(filters.NumberFilter):
    def filter(self, qs, value):
        validate_thousand(value)
        return super().filter(qs, value)

class OverlappingPriceRangeFilter(Filter):
    def filter(self, qs, value):
        if value:
            min_price, max_price = value
            # Check for overlapping ranges using Q objects
            overlapping = Q(price__lte=max_price, price__gte=min_price)
            return qs.filter(overlapping)
        return qs

class OverlappingDateRangeFilter(Filter):
    def filter(self, qs, value):
        if value:
            start_date, end_date = value
            # Check for overlapping ranges using Q objects
            overlapping = Q(start_date__lte=end_date, end_date__gte=start_date)
            return qs.filter(overlapping)
        return qs

class MainPostFilter(filters.FilterSet):
    genre = filters.ChoiceFilter(choices=MainPost.GENRE_CHOICES)
    location = filters.ChoiceFilter(choices=MainPost.LOCATION_CHOICES)
    price_range = OverlappingPriceRangeFilter()
    date_range = OverlappingDateRangeFilter()

    class Meta:
        model = MainPost
        fields = ['genre', 'location', 'price_range', 'date_range']

class MainPostViewSet(viewsets.ModelViewSet):
    queryset = MainPost.objects.annotate(
        like_cnt=Count(
            "reactions", filter=Q(reactions__reaction="like"), distinct=True
        ),

    )
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = MainPostFilter

    filterset_fields = ["title"]
    search_fields = ["title"]
    #ordering_fields = ["-created_at"]
    serializer_class = MainPostSerializer
    permission_classes = [IsAdminUser]
    
    def get_serializer_class(self):
        if self.action == "list":
            return MainPostListSerializer
        return MainPostSerializer

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
            existing_reaction = MainPostReaction.objects.get(mainpost=mainpost, user=user, reaction="like")
            existing_reaction.delete()
            return Response({"detail": "좋아요 취소"}, status=status.HTTP_200_OK)
        except MainPostReaction.DoesNotExist:
            MainPostReaction.objects.create(compost=compost, user=user, reaction="like")
            return Response({"detail": "좋아요!"}, status=status.HTTP_201_CREATED)

#별점 높은 순
    @action(detail=False, methods=["GET"])
    def rating(self, request):
        mainposts = MainPost.objects.annotate(average_rating=Avg('mainreviews__rating')).order_by('-average_rating')
        serializer = MainPostListSerializer(mainposts, many=True)
        return Response(serializer.data)

#후기많은 순
    @action(detail=False, methods=["GET"])
    def reviews(self, request):
        mainposts = self.queryset.order_by("-mainreviews_cnt")
        serializer = MainPostListSerializer(mainposts, many=True)
        return Response(serializer.data)

#리뷰 detail 뷰셋
class MainReviewViewSet(
    viewsets.GenericViewSet, 
    mixins.RetrieveModelMixin, 
    mixins.DestroyModelMixin,
    mixins.ListModelMixin
    ):
    queryset = MainReview.objects.all()
    serializer_class = MainReviewSerializer

    def get_permissions(self):
        if self.action in ["create", "destroy"]:
            return [IsOwnerOrReadOnly()]
        return []

    def get_objects(self):
        obj = super().get_object()
        return obj

#리뷰 작성 뷰셋 
class MainReviewWriteViewSet(
    viewsets.GenericViewSet, 
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    ):
    serializer_class = MainReviewSerializer
    permission_classes = [IsAuthenticated]

#    def get_permissions(self):
#        if self.action in ['create', 'destroy']:
#            return [IsAuthenticated()]
#        return []

    def get_queryset(self):
        mainpost = self.kwargs.get("mainpost_id")
        queryset = MainReview.objects.filter(mainpost_id=mainpost)
        return queryset

    def create(self, request, mainpost_id=None):
        mainpost = get_object_or_404(MainPost, id=mainpost_id)
        ticket_id = request.data.get('ticket')
        if not ticket_id:
            return Response({"error": "티켓을 선택해주세요."}, status=400)
        ticket = get_object_or_404(Ticket, id=ticket_id)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(mainpost=mainpost, ticket=ticket)
        return Response(serializer.data)

# 리뷰 댓글 detail 관련 뷰셋
class MainReviewCommentViewSet(
    viewsets.GenericViewSet, 
    mixins.DestroyModelMixin, 
    mixins.ListModelMixin, 
    mixins.RetrieveModelMixin
    ):
    queryset = MainReviewComment.objects.all()
    serializer_class = MainReviewCommentSerializer

    # 읽기만 가능
    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            return [IsOwnerOrReadOnly()]
        return []

#리뷰 댓글 작성 관련 뷰셋
class MainReviewCommentWriteViewSet(
    viewsets.GenericViewSet, 
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    ):
    queryset = MainReviewComment.objects.all()
    serializer_class = MainReviewCommentSerializer

    def get_queryset(self):
        mainreview = self.kwargs.get("mainreview_id")
        queryset = ComReply.objects.filter(mainreview_id=mainreview)
        return queryset
    
    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            return [IsOwnerOrReadOnly()]
        return []
    
    def create(self, request, mainreview_id=None):
        mainreview = get_object_or_404(MainReview, id=mainreview_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(mainreview=mainreview)
        return Response(serializer.data)

