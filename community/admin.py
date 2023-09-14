from django.contrib import admin
from .models import *

class ComPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'writer', 'created_at', 'updated_at', 'category', 'views',)
    search_fields = ('title', 'writer__nickname',)

admin.site.register(ComPost, ComPostAdmin)
