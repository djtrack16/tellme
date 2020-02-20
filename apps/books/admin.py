from django.contrib import admin
from books.models import Book, Entry


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'creation_date', 'last_update_date')
    list_filter = ('author', 'title')

class EntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'book', 'creation_date', 'last_update_date')
    list_filter = ('book',)


admin.site.register(Book, BookAdmin)
admin.site.register(Entry, EntryAdmin)
