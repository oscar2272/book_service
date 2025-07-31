from django.contrib import admin
from . models import Book, Author

class AuthorAdmin(admin.ModelAdmin):
    ist_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('id',)

class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'published_at')
    list_filter = ('author', 'published_at')
    search_fields = ('title', 'author__name')
    ordering = ('-published_at',)
    
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)