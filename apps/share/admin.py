from django.contrib import admin
from share.models import Shared

class ShareAdmin(admin.ModelAdmin):
    list_display = ('book', 'entry', 'from_user', 'to_user', 'date')
    list_filter = ('from_user', 'to_user', 'book')
    list_display_links = ('book', 'entry')

admin.site.register(Shared, ShareAdmin)
