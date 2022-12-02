from django.contrib import admin
from .models import Hotel, HotelImage


class TabularInImages(admin.TabularInline):
    model = HotelImage
    extra = 1
    fields = ['image']


class HotelAdmin(admin.ModelAdmin):
    model = Hotel
    inlines = [TabularInImages]

admin.site.register(Hotel, HotelAdmin)
