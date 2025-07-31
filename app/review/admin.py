from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    class ReviewAdmin(admin.ModelAdmin):
        list_display = ("review_id", "book_id", "user_id", "rating", "created_at","updated_at")
        search_fields = ("content",)
        list_filter = ("rating", "created_at")

#어셔랑 북이랑 리뷰 받을거를 넣어라. 
# Register your models here.
