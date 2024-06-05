from django.contrib import admin
from .models import Board, Reply, Like

# Register your models here.
@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    pass

@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    pass

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    pass