from django.shortcuts import render, get_object_or_404, redirect
from .models import Board, Reply, Like
from .forms import BoardForm, ReplyForm
from django.core.paginator import Paginator
from django.db.models import Count


# Create your views here.
def index(request):
    boards = Board.objects.all().order_by("-id")
    paginator = Paginator(boards, 10)

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    current_page = page_obj.number
    range_size = 5
    half_range = range_size // 2

    start_page = max(current_page - half_range, 1)
    end_page = min(start_page + range_size - 1, paginator.num_pages)

    page_range = range(start_page, end_page + 1)

    board_data = []

    for board in page_obj:
        likes_count = Like.objects.filter(board=board).count()
        comments_count = Reply.objects.filter(board=board).count()
        board_data.append({
            'board':board,
            'likes_count': likes_count,
            'comment_count': comments_count,
        })

    return render(request,'boards/index.html', 
                  context={'page_obj': page_obj, 'page_range': page_range, 'board_data' : board_data})


# 게시글 목록
def board_list(request):
    boards = Board.objects.annotate(
        likes_count = Count('board_likes'),
        comments_count = Count('reply')
    ).order_by('-id')

    paginator = Paginator(boards, 10)

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    current_page = page_obj.number
    range_size = 5
    half_range = range_size // 2

    start_page = max(current_page - half_range, 1)
    end_page = min(start_page + range_size - 1, paginator.num_pages)

    page_range = range(start_page, end_page + 1)

    return render(request, 'boards/board_list.html', context={'page_obj': page_obj, 'page_range': page_range})


# 게시글 등록
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
    board = get_object_or_404(Board, pk=pk)
    comment_list = Reply.objects.filter(board=pk).order_by("-created_at")

    return render(request, 'boards/board_read.html', context = {"board": board, "comment_list": comment_list})


# 댓글 등록 
def comment_create(request,pk):
    board = get_object_or_404(Board, pk=pk)
    comment_list = Reply.objects.filter(board=pk).order_by("-created_at")

    if request.method == "POST":
        form = ReplyForm(request.POST)

        if form.is_valid():
            comments = form.save(commit=False)
            comments.author = request.user
            comments.board = board
            comments.save()
            return redirect("boards:board_read", pk=pk)
    
    else:
        form = ReplyForm()
    return render(request, "boards/board_read.html", context = {
        "form" : form,
        "board" : board,
        "comment_list" : comment_list,
    })
