from django.shortcuts import render

# Create your views here.
def profile(request):
    return render(request, 'accounts/profile.html')

def purchase(request):
    return render(request, 'accounts/purchase_detail.html')

def sales(request):
    return render(request, 'accounts/sales_detail.html')

def download(request):
    return render(request, 'accounts/download_detail.html')

def following(request):
    return render(request, 'accounts/following.html')