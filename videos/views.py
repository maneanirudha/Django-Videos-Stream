from django.http import StreamingHttpResponse, HttpResponse
from django.shortcuts import get_object_or_404
from .models import Video
import os
from rest_framework.decorators import api_view
import ffmpeg
import subprocess

@api_view(['GET'])
def video_stream(request, video_id, quality):
    video = get_object_or_404(Video, id=video_id)
    input_path = video.video_file.path

    resolutions = {
        '240p': '426x240',
        '360p': '640x360',
        '480p': '854x480',
        '720p': '1280x720',
        '1080p': '1920x1080',
    }
    
    if quality not in resolutions:
        return HttpResponse(status=400)  # Bad Request for invalid quality
    
    resolution = resolutions[quality]

    command = [
        'ffmpeg',
        '-i', input_path,
        '-vf', f'scale={resolution}',
        '-f', 'mp4',
        '-movflags', 'frag_keyframe+empty_moov',
        'pipe:1'
    ]
    
    def stream_video():
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while True:
            output = process.stdout.read(8192)
            if not output:
                break
            yield output
        process.stdout.close()

    response = StreamingHttpResponse(stream_video(), content_type='video/mp4')
    response['Content-Disposition'] = f'inline; filename="{video.title}.mp4"'
    return response
