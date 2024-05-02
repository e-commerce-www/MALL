from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from twilio.rest import Client
from .forms import SellerApplyForm
from .models import Seller
from apps.songs.models import Song

CLIENT = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

def send_verification_code(phone_number):
    otp_verification = CLIENT.verify.services(settings.TWILIO_SERVICE_SID).verifications.create(to=phone_number, channel='sms')

@login_required
def seller_apply(request):
    if request.method == 'POST':
        form = SellerApplyForm(request.POST)
        if form.is_valid():
            seller = form.save(commit=False)  # Don't save yet
            seller.user = request.user
            seller.save()
            
            # Update user's is_seller field to True
            # request.user.is_seller = True
            # request.user.save()

            phone_number = form.cleaned_data.get('phone_number')
            send_verification_code('+82'+phone_number[1:])

            return redirect('sellers:seller_verify')        
    else:
        form = SellerApplyForm()
    
    return render(request, 'sellers/apply.html', {'form': form})

@login_required
def seller_verify(request):
    if request.method == 'POST':
        verify_code = request.POST['verification_code']
        phone_number = '+82' + Seller.objects.get(user=request.user).phone_number[1:]
        verify_check = CLIENT.verify.services(settings.TWILIO_SERVICE_SID).verification_checks.create(to=phone_number, code=verify_code)
        
        if verify_check.status == 'approved':
            
            request.user.is_seller = True
            request.user.save()

            return render(request, 'sellers/verify.html', context={'code_valid': '판매자 등록이 정상적으로 완료되었습니다.'})
        else:
            return render(request, 'sellers/verify.html', context={'code_invalid': '인증코드가 일치하지 않습니다.'})
    else:
        return render(request, 'sellers/verify.html')

def seller_detail(request, pk):
    seller = Seller.objects.get(user_id=pk)
    songs = Song.objects.filter(seller=seller)
    
    return render(request, 'sellers/seller_detail.html', context={'seller': seller, 'songs': songs})