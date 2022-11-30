from django.contrib import admin
from .models import Hotel, HotelImage



class TabularInImages(admin.TabularInline):
    model = HotelImage
    extra = 1
    fields = ['image']


class PostAdmin(admin.ModelAdmin):
    model = Hotel
    inlines = [TabularInImages]

admin.site.register(Hotel, PostAdmin)