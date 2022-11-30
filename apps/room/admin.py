from django.contrib import admin
from .models import Room, RoomImage, RoomNum



class TabularInRoom(admin.TabularInline):
    model = RoomNum
    extra = 1
    fields = ['room_name', 'room_no', 'is_booked']




class TabularInlineImage(admin.TabularInline):
    model = RoomImage
    extra = 0
    fields = ['image']


class RoomAdmin(admin.ModelAdmin):
    model = Room
    inlines = [TabularInlineImage, TabularInRoom]


admin.site.register(Room, RoomAdmin)