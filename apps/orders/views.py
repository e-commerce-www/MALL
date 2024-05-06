from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Order


# @login_required
# def order_list(request):
#     order_list = get_list_or_404(Order, user=request.user)
#     paginator = Paginator(order_list, 10)
    
#     page_number = request.GET.get('page', 1)
#     page_obj = paginator.get_page(page_number)
    
#     return render(request, 'orders/order_list.html', context={'page_obj': page_obj})

# @login_required
# def order_detail(request, pk):
#     order = get_object_or_404(Order, pk=pk, user=request.user)
    
#     return render(request, 'orders/order_detail.html', context={'order': order})