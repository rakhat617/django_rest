from django.contrib import admin

from images.models import Images

# Register your models here.

@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    model = Images