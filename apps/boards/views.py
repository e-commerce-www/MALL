import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Board
from apps.likes.models import BoardLike, Bookmark
from .forms import BoardForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.conf import settings
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from .utils import *


# Create your views here.

def get_disqus_comment_count(disqus_id):
    api_url = 'https://disqus.com/api/3.0/threads/details.json'
    params = {
        'api_key': settings.DISQUS_API_KEY,
        'forum': settings.DISQUS_SHORTNAME_2,
        'thread:ident': disqus_id
    }

    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        data = response.json()
        print(data)
        return data['response']['posts']
    
    elif response.status_code == 400 and response.json().get('code') == 2:
        print(f"Thread not found for ID {disqus_id}")
        return 0  # 스레드가 존재하지 않는 경우
    
    # print("Error: ", response.status_code, response.json())
    return 0


# 게시글 목록
def board_list(request):
    sort = request.GET.get('sort','latest')
    search = request.GET.get('search')

    boards = Board.objects.annotate(
        likes_count = Count('board_likes')
    )

    ## 게시글 정렬
    if sort == 'popular':
        boards = boards.order_by('-likes_count', '-created_at')
    else:
        boards = boards.order_by('-created_at')


    ## 게시글 검색
    if search:
        search_no_spaces = search.replace(' ', '')
        english_search = get_english_variants(search_no_spaces)
        
        search_query = Q(title__icontains=search) | Q(content__icontains=search)
        english_query = Q(title__icontains=english_search) | Q(content__icontains=english_search)
        
        boards = boards.filter(search_query | english_query)


    ## 페이지네이션 적용
    paginator = Paginator(boards, 10)
    page_number = request.GET.get('page', 1)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)


    current_page = page_obj.number
    range_size = 5
    half_range = range_size // 2

    start_page = max(current_page - half_range, 1)
    end_page = min(start_page + range_size - 1, paginator.num_pages)
    page_range = range(start_page, end_page + 1)

    return render(request, 'boards/board_list.html', context={
        'page_obj': page_obj, 
        'page_range': page_range, 
        'sort':sort,
        'search' : search,
    })


def comment_count(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        board_id = request.GET.get('board_id')
        disqus_id = f"board-{board_id}"
        comment_count = get_disqus_comment_count(disqus_id)
        
        # print(f"comment count : {disqus_id} : ", comment_count) // 댓글 수 확인 위한 코드

        return JsonResponse({'comment_count': comment_count})
    return JsonResponse({'comment_count': 0})


# 게시글 등록
@login_required
def board_create(request):
    if request.method == "POST":
        form = BoardForm(request.POST)

        if form.is_valid():
            board = form.save(commit=False)
            board.author = request.user
            board.save()
            return redirect('boards:board_list')
        
    else:
        form = BoardForm()

    return render(request, 'boards/board_create.html', context = {'form': form})


# 게시글 보기
def board_read(request,pk):
    board = Board.objects.annotate(likes_count=Count('board_likes')).get(pk=pk)
    board_like = BoardLike.objects.filter(user=request.user, board=board).exists()
    bookmark = Bookmark.objects.filter(user=request.user, board=board).exists()

    disqus_short = f"{settings.DISQUS_SHORTNAME_2}"
    disqus_id = f"board-{board.id}"
    disqus_url = f"{settings.DISQUS_MY_DOMAIN_2}{board.get_absolute_url()}"
    disqus_title = f"{board.title}"

    context = {
        "board": board, 
        "board_like" : board_like,
        "bookmark" : bookmark,
        "disqus_short": disqus_short,
        "disqus_id": disqus_id,
        "disqus_url": disqus_url,
        "disqus_title": disqus_title,
        }

    return render(request, 'boards/board_read.html', context = context)


# 게시글 수정
def board_update(request, pk):
    board = get_object_or_404(Board, pk=pk)

    if request.method == 'POST':
        form = BoardForm(request.POST, instance=board)
        if form.is_valid():
            board = form.save(commit=False)
            board.save()
            messages.success(request, '게시글이 성공적으로 수정되었습니다.')
            return redirect("boards:board_read", pk=pk)
        
    else:
        form = BoardForm(instance=board)

    return render(request, 'boards/board_update.html', context={"form":form, "board":board})


# 게시글 삭제
def board_delete(request, pk):
    board = get_object_or_404(Board, pk=pk)
    board.delete()
    messages.success(request, '글을 삭제했습니다.')
    return redirect("boards:board_list")


# 북마크 글
def bookmarked_boards(request):
    bookmarks = Bookmark.objects.filter(user=request.user).select_related('board').order_by('-created_at')

    paginator = Paginator(bookmarks, 10)

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    current_page = page_obj.number
    range_size = 5
    half_range = range_size // 2

    start_page = max(current_page - half_range, 1)
    end_page = min(start_page + range_size - 1, paginator.num_pages)

    page_range = range(start_page, end_page + 1)

    return render(request, 'boards/bookmark_list.html', context={'page_obj': page_obj, 'page_range': page_range,})
