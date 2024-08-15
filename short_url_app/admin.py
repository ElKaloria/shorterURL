from django.contrib import admin
from .models import ShortUrl


# Register your models here.

@admin.register(ShortUrl)
class URLAdmin(admin.ModelAdmin):
    list_display = ('original_url', 'short_url', 'request_count', 'created_at', 'user')
    search_fields = ('original_url', 'short_url')
    ordering = ['-created_at']

