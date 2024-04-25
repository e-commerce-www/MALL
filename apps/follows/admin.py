from django.contrib import admin
from .models import Follows

# Register your models here.
@admin.register(Follows)
class FollowsAdmin(admin.ModelAdmin):
    pass