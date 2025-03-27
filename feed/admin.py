from django.contrib import admin

from feed.models import Like, Post, Comment, ChatRoom, Message

# Register your models here.

admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ("id", "user1", "user2", "created_at")  # Admin panel me columns
    search_fields = ("user1__username", "user2__username")  # Search feature enable
    list_filter = ("created_at",)  # Filter option

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "chat_room", "sender", "content", "created_at") 
    search_fields = ("sender__username", "chat_room__id")  
    list_filter = ("created_at",)  

