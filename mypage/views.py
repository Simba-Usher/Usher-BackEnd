import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TicketSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *

def value_to_str(value):
    if pd.isna(value):
        return ""  
    return str(value) 

class TicketView(APIView):
    def post(self, request):
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            ticket_number = serializer.validated_data['ticket_number']
            #memo = serializer.validated_data.get('memo', None)

            
            # pandas로 엑셀 데이터 불러오기
            df = pd.read_excel('static/KOPIS_data1.xlsx')
            
            # 티켓 번호를 기준으로 원하는 데이터 찾기
            row_data = df[df['입장권고유번호'] == ticket_number]

            if not row_data.empty:
                desired_data = {
                    "performance": value_to_str(row_data['공연코드'].values[0]),
                    "performance_location": value_to_str(row_data['공연장코드'].values[0]),
                    "performance_date": value_to_str(row_data['공연일시'].values[0]),
                    "reservation_site": value_to_str(row_data['공연일시'].values[0]),
                    "discount_method": value_to_str(row_data['할인종류명(전송처)'].values[0]),
                    "price": value_to_str(row_data['예매/취소금액'].values[0]),
                }

                #ticket, created = Ticket.objects.get_or_create(
                #    ticket_number=ticket_number,
                #    defaults={"memo": memo}
                #)
                #if not created and memo:
                #    ticket.memo = memo
                #    ticket.save()

                return Response(desired_data, status=200)
            else:
                return Response({"error": "유효하지 않은 티켓입니다."}, status=400)
        return Response(serializer.errors, status=400)

