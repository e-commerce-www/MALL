from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from apps.songs.models import Song
from .models import Payment
from django.http import Http404
from django.conf import settings


@login_required
def payment_pay(request, pk):
    song = Song.objects.get(pk=pk)

    payment = Payment.objects.create(
        user=request.user,
        song=song,
        name=song.title,
        amount=song.price,
    )

    payment_props = {
        "pg": "kakaopay",
        "merchant_uid": payment.merchant_uid,
        "name": payment.name,
        "amount": payment.amount,
    }

    payment_verify_url = reverse("payments:payment_verify", args=[payment.pk])

    return render(
        request,
        "payments/payment_pay.html",
        {
            "portone_shop_id": settings.PORTONE_SHOP_ID,
            "payment_props": payment_props,
            "payment_verify_url": payment_verify_url,
        },
    )


@login_required
def payment_verify(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    if request.user == payment.user:
        payment.verify()
        return redirect("payments:payment_detail", pk=payment.pk)
    else:
        raise Http404("No such payment exists.")


@login_required
def payment_detail(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    if request.user == payment.user:
        return render(
            request,
            "payments/payment_detail.html",
            context={
                "payment": payment,
            },
        )
    else:
        raise Http404("No such payment exists.")
