from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'nickname', 'grade']  # admin 페이지의 목록에서 보여줄 필드들
    list_filter = ['grade']  # grade 필드에 대한 필터 옵션을 제공
    search_fields = ['email', 'nickname']  # 검색 기능 제공을 위한 필드 지정
