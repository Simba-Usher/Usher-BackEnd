from django.contrib import admin
from .models import MainPost

# 모델을 admin 페이지에 등록하기 위한 admin 클래스
class MainPostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'content', 'price', 'start_date', 'end_date']  # 목록에 보여줄 필드들
    search_fields = ['title', 'content']  # 검색 기능을 사용할 필드들
    list_filter = ['genre', 'location']  # 필터 기능을 사용할 필드들
    ordering = ['-start_date']  # 기본 정렬 순서

admin.site.register(MainPost, MainPostAdmin)
