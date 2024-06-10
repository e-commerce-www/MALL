from django.contrib import admin
from .models import Like, BoardLike, Bookmark

# Register your models here.
@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    pass

@admin.register(BoardLike)
class BoardLikeAdmin(admin.ModelAdmin):
    pass

@admin.register(Bookmark)
class BoardLikeAdmin(admin.ModelAdmin):
    pass