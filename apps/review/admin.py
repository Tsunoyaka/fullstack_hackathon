from django.contrib import admin
from .models import Comment, CommentImage


class TabularInImages(admin.TabularInline):
    model = CommentImage
    extra = 1
    fields = ['image']


class PostAdmin(admin.ModelAdmin):
    model = Comment
    inlines = [TabularInImages]

admin.site.register(Comment, PostAdmin)