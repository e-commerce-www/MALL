from django.contrib import admin
from .models import Like

# Register your models here.
@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    pass