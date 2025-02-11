from django.contrib import admin

from feed.models import Like, Post, Comment

# Register your models here.

admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)
