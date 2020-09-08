from django.contrib import admin
from .models import Comic, Images


class ImageInlineAdmin(admin.StackedInline):
    model = Images


class ComicAdmin(admin.ModelAdmin):
    inlines = [ImageInlineAdmin]

    class Meta:
        model = Comic


admin.site.register(Comic, ComicAdmin)
