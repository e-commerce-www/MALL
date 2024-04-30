from django.shortcuts import render

# Create your views here.
def seller_apply(request):
    return render(request, 'sellers/apply.html')