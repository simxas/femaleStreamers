from django.contrib import admin
from .models import Streamer

class StreamerModelAdmin(admin.ModelAdmin):
    list_display = ["display_name", "timestamp", "updated"]
    list_display_links = ["timestamp", "updated"]
    list_editable = ["display_name"]
    list_filter = ["updated", "timestamp"]
    search_fields = ["name", "display_name"]
    class Meta:
        model = Streamer

admin.site.register(Streamer, StreamerModelAdmin)
