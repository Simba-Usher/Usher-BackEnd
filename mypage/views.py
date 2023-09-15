import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, mixins, generics, status
from django.shortcuts import get_object_or_404
from rest_framework.mixins import UpdateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView, ListAPIView

from .models import *
from .serializers import *

from main.serializers import MainPostListSerializer, MainReviewSerializer
from community.serializers import ComPostListSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response


def value_to_str(value):
    if pd.isna(value):
        return ""  
    return str(value) 

class TicketView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, ticket_id=None, *args, **kwargs):
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            ticket_number = serializer.validated_data['ticket_number']
            #ticket_memo = serializer.validated_data.get('ticket_memo', None)
            
            # pandas로 엑셀 데이터 불러오기
            df = pd.read_excel('static/KOPIS_data1.xlsx')
            
            
            # 티켓 번호를 기준으로 원하는 데이터 찾기
            row_data = df[df['입장권고유번호'] == ticket_number]

            if not row_data.empty:
                desired_data = {
                    "performance": value_to_str(row_data['공연코드'].values[0]),
                    "performance_location": value_to_str(row_data['공연장코드'].values[0]),
                    "performance_date": value_to_str(row_data['공연일시'].values[0]),
                    "reservation_site": value_to_str(row_data['전송사업자명'].values[0]),
                    "discount_method": value_to_str(row_data['할인종류명(전송처)'].values[0]),
                    "price": float(row_data['예매/취소금액'].values[0]) if pd.notna(row_data['예매/취소금액'].values[0]) else 0,                }

                ticket, created = Ticket.objects.update_or_create(
                    ticket_number=ticket_number,
                    
                    defaults={
                        "writer": request.user,
                        **desired_data 
                    }
                )

                desired_data["id"] = ticket.id
                
                return Response(desired_data, status=200)
            else:
                return Response({"error": "유효하지 않은 티켓입니다."}, status=400)
        return Response(serializer.errors, status=400)

    def get(self, request, ticket_id=None):
            if ticket_id:  #티켓 하나 가져오기
                ticket = get_object_or_404(Ticket, id=ticket_id)
                serializer = TicketSerializer(ticket)
            else:  #티켓 다 가져오기
                user_tickets = Ticket.objects.filter(writer=request.user)
                serializer = TicketSerializer(user_tickets, many=True)
            
            return Response(serializer.data, status=200)
    
    def put(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, id=ticket_id)
        serializer = TicketSerializer(ticket, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, id=ticket_id)
        if ticket.writer != request.user:
            return Response({"error": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        ticket.delete()
        return Response({"message": "티켓이 성공적으로 삭제되었습니다."}, status=status.HTTP_200_OK)


class MemoViewSet(viewsets.ModelViewSet):
    queryset = Memo.objects.all()
    permission_classes = [IsAuthenticated]

    serializer_class = MemoSerializer

    def get_queryset(self):
        return Memo.objects.filter(writer=self.request.user)

class ProfileUpdateView(UpdateModelMixin, generics.GenericAPIView):
    serializer_class = ProfileUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

class LikedMainPostListView(generics.ListAPIView):
    serializer_class = MainPostListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return user.liked_posts.all()
    
class LikedComPostListView(ListModelMixin, GenericAPIView):
    serializer_class = ComPostListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.liked_composts.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class MyMainReviewListView(ListAPIView):
    serializer_class = MainReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MainReview.objects.filter(writer=self.request.user)

class MyComPostListView(ListAPIView):
    serializer_class = ComPostListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ComPost.objects.filter(writer=self.request.user)

class TicketMemoView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, id=ticket_id)
        memo_data = request.data.get('ticket_memo', '')
        ticket.ticket_memo = memo_data
        ticket.save()
        return Response({"message": "메모가 성공적으로 추가/업데이트 되었습니다."}, status=200)

    def put(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, id=ticket_id)
        memo_data = request.data.get('ticket_memo', '')
        ticket.ticket_memo = memo_data
        ticket.save()
        return Response({"message": "메모가 성공적으로 수정되었습니다."}, status=200)
