from django.contrib import admin
from .models import Comment, Dislike, Like

admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Dislike)
