from django.contrib import admin
from .models import Video

class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at', 'video_file', 'thumbnail')
    search_fields = ('title', 'description')
    list_filter = ('uploaded_at',)
    ordering = ('-uploaded_at',)

admin.site.register(Video, VideoAdmin)
