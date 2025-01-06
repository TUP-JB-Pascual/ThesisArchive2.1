from django.contrib import admin
from .models import Thesis, TempURL

# Register your models here.
@admin.register(Thesis)
class ThesisAdmin(admin.ModelAdmin):
    list_display = ['title', 'poster', 'get_tags']

    def get_tags(self, obj):
        return ", ".join(o for o in obj.tags.names())

@admin.register(TempURL)
class ThesisAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'status', 'url_status', 'rejection_reason']
