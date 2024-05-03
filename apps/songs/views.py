from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import StreamingHttpResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.http import JsonResponse, Http404
from .models import Song
from .services import ranked_songs
import boto3
import os


def song_list(request):
    song_list = Song.objects.all()
    paginator = Paginator(song_list, 10)

    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    current_page = page_obj.number
    range_size = 5
    half_range = range_size // 2

    start_page = max(current_page - half_range, 1)
    end_page = min(start_page + range_size - 1, paginator.num_pages)

    page_range = range(start_page, end_page + 1)

    return render(
        request,
        "songs/song_list.html",
        context={"page_obj": page_obj, "page_range": page_range},
    )


def song_detail(request, pk):
    song = get_object_or_404(Song, pk=pk)

    viewed_songs = request.session.get("viewed_songs", [])

    if song.id not in viewed_songs:
        viewed_songs.insert(0, song.id)
        viewed_songs = viewed_songs[:10]

    request.session["viewed_songs"] = viewed_songs

    return render(request, "songs/song_detail.html", context={"song": song})

# 로컬 테스트시 사용
def song_stream(request, pk):
    song = get_object_or_404(Song, pk=pk)
    file_path = os.path.join(settings.MEDIA_ROOT, song.mp3.name)

    def file_iterator(file_name, chunk_size=8192):
        with open(file_name, mode="rb") as file:
            while True:
                data = file.read(chunk_size)
                if not data:
                    break
                yield data

    response = StreamingHttpResponse(file_iterator(file_path))
    response["Content-Type"] = "audio/mpeg"
    response["Content-Disposition"] = 'inline; filename="{}"'.format(
        os.path.basename(file_path)
    )
    return response

# AWS S3 연동 시 사용
# def song_stream(request, pk):
#     song = get_object_or_404(Song, pk=pk)

#     # AWS S3 설정
#     s3 = boto3.client(
#         "s3",
#         aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
#         aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
#         region_name=settings.AWS_S3_REGION_NAME,
#     )

#     bucket_name = settings.AWS_STORAGE_BUCKET_NAME
#     s3_file_key = song.mp3.name

#     try:
#         # S3 객체의 메타데이터 가져오기
#         file_obj = s3.get_object(Bucket=bucket_name, Key=s3_file_key)
#     except s3.exceptions.NoSuchKey:
#         raise Http404("File does not exist on S3")

#     # 파일 스트리밍을 위한 함수
#     def file_iterator(file_obj, chunk_size=8192):
#         for chunk in iter(lambda: file_obj["Body"].read(chunk_size), b""):
#             yield chunk

#     # 스트리밍 응답 설정
#     response = StreamingHttpResponse(file_iterator(file_obj))
#     response["Content-Type"] = "audio/mpeg"
#     response["Content-Disposition"] = (
#         f'inline; filename="{os.path.basename(s3_file_key)}"'
#     )
#     return response


def song_lyrics(request):
    song_id = request.GET.get("songid")
    if not song_id:
        return HttpResponse("Song ID not provided", status=400)
    try:
        song_lyrics = Song.objects.get(pk=song_id).lyrics
        return JsonResponse({"success": song_lyrics})
    except ObjectDoesNotExist:
        return HttpResponse("Song not found", status=404)
    except Exception as e:
        return HttpResponse(str(e), status=500)


def song_recent(request):
    songs = Song.objects.all().order_by("-created_at")
    page_number = request.GET.get("page", 1)
    paginator = Paginator(songs, 10)
    page_obj = paginator.get_page(page_number)
    return render(request, "songs/song_list_recent.html", {"page_obj": page_obj})
