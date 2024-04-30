from django.contrib import admin
from .models import Seller
# Register your models here.

@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    pass