from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from twilio.rest import Client
from .forms import SellerApplyForm
from apps.songs.forms import SongUploadForm, SongEditForm
from django.core.paginator import Paginator
from .models import Seller
from apps.songs.models import Song

CLIENT = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)


def send_verification_code(phone_number):
    otp_verification = CLIENT.verify.services(
        settings.TWILIO_SERVICE_SID
    ).verifications.create(to=phone_number, channel="sms")


@login_required
def seller_apply(request):
    if request.method == "POST":
        form = SellerApplyForm(request.POST)
        if form.is_valid():
            seller = form.save(commit=False)  # Don't save yet
            seller.user = request.user
            seller.save()

            phone_number = form.cleaned_data.get("phone_number")
            send_verification_code("+82" + phone_number[1:])

            return redirect("sellers:seller_verify")
    else:
        form = SellerApplyForm()

    return render(request, "sellers/apply.html", {"form": form})


@login_required
def seller_verify(request):
    if request.method == "POST":
        verify_code = request.POST["verification_code"]
        phone_number = "+82" + Seller.objects.get(user=request.user).phone_number[1:]
        verify_check = CLIENT.verify.services(
            settings.TWILIO_SERVICE_SID
        ).verification_checks.create(to=phone_number, code=verify_code)

        if verify_check.status == "approved":

            request.user.is_seller = True
            request.user.save()

            return render(
                request,
                "sellers/verify.html",
                context={"code_valid": "판매자 등록이 정상적으로 완료되었습니다."},
            )
        else:
            return render(
                request,
                "sellers/verify.html",
                context={"code_invalid": "인증코드가 일치하지 않습니다."},
            )
    else:
        return render(request, "sellers/verify.html")


# @login_required
# def seller_detail(request, pk):
#     seller = Seller.objects.get(user_id=pk)
#     songs = Song.objects.filter(seller=seller)

#     return render(
#         request,
#         "sellers/seller_detail.html",
#         context={"seller": seller, "songs": songs},
#     )


@login_required
def seller_upload(request):
    if request.method == "POST":
        form = SongUploadForm(request.POST, request.FILES)
        if form.is_valid():
            song = form.save(commit=False)
            seller_instance = request.user.seller_set.first()
            song.seller = seller_instance
            song.save()
            return redirect("sellers:seller_songs")
        else:
            return render(request, "sellers/seller_upload.html", context={"form": form})
    else:
        form = SongUploadForm()
    return render(request, "sellers/seller_upload.html", context={"form": form})


@login_required
def seller_edit(request, pk):
    song = get_object_or_404(Song, pk=pk)
    if request.method == "POST":
        form = SongEditForm(request.POST, request.FILES, instance=song)
        if form.is_valid():
            form.save()
            return redirect("sellers:seller_songs")
    else:
        form = SongEditForm(instance=song)
    return render(request, "sellers/seller_edit.html", context={"form": form})


@login_required
def seller_songs(request):
    song_list = Song.objects.filter(seller__user=request.user)
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
        "sellers/seller_songs.html",
        context={"page_obj": page_obj, "page_range": page_range},
    )


def seller_artist(request, pk):
    seller = Seller.objects.get(user_id=pk)

    songs = Song.objects.filter(seller=seller)

    paginator = Paginator(songs, 10)

    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    current_page = page_obj.number
    range_size = 5
    half_range = range_size // 2

    start_page = max(current_page - half_range, 1)
    end_page = min(start_page + range_size - 1, paginator.num_pages)

    page_range = range(start_page, end_page + 1)

    context = {
        'seller': seller,
        'page_obj': page_obj,
        'page_range': page_range,
    }
    
    return render(
        request,
        "sellers/seller_artist.html",
        context=context
    )
