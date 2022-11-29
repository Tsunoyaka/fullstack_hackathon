from django.contrib import admin
from .models import Room, RoomImage

class TabularInlineImage(admin.TabularInline):
    model = RoomImage
    extra = 0
    fields = ['image']


class RoomAdmin(admin.ModelAdmin):
    model = Room
    inlines = [TabularInlineImage, ]


admin.site.register(Room, RoomAdmin)