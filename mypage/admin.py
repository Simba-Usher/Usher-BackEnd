from django.contrib import admin
from .models import Ticket, Memo

# Ticket 모델의 Admin 정의
class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'writer', 'ticket_number', 'performance', 'performance_location', 'performance_date', 'reservation_site', 'discount_method', 'price', 'ticket_memo']
    search_fields = ['ticket_number', 'performance']
    list_filter = ['performance_location', 'reservation_site']

# Memo 모델의 Admin 정의
class MemoAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'location', 'date', 'content']
    search_fields = ['title', 'location']
    list_filter = ['location']

# 모델을 admin 사이트에 등록
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Memo, MemoAdmin)
