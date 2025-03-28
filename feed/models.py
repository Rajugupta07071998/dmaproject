from django.db import models

# Create your models here.

from django.utils.timezone import now
from datetime import timedelta
from account.models import User
from core.models import BaseModel
from django.core.exceptions import ValidationError



def validate_file_extension(value):
    """ Validate if the uploaded file is an image or video based on extension """
    image_extensions = ['jpg', 'jpeg', 'png', 'gif', 'webp']
    video_extensions = ['mp4', 'avi', 'mov', 'mpeg', 'mkv', 'webm']

    ext = value.name.split('.')[-1].lower()  

    if ext in image_extensions:
        return 'image'
    elif ext in video_extensions:
        return 'video'
    else:
        raise ValidationError("Unsupported file format! Only images and videos are allowed.")


class Post(BaseModel):
    """
    Represents a post made by a user. It can contain media (image/video), a caption,
    hashtags, and maintains view count and archive status.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts"  # A user can have multiple posts
    )
    media = models.FileField(upload_to='Post/medias/')  
    caption = models.TextField(blank=True, null=True)  # Caption text
    hashtags = models.CharField(max_length=500, blank=True, null=True)  # List of hashtags (stored as JSON)
    views_count = models.PositiveBigIntegerField(default=0)  
    media_type = models.CharField(max_length=10, blank=True, null=True)
    is_video = models.BooleanField(default=False)
    extension = models.CharField(max_length=10, blank=True, null=True)  
    duration = models.FloatField(blank=True, null=True)  
    category = models.CharField(max_length=50, blank=True, null=True)
    video_size = models.FloatField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["-created_at"]),
        ]

    def save(self, *args, **kwargs):
        """ Auto-detect media type based on file extension before saving """
        if self.media:
            self.media_type = validate_file_extension(self.media)  # Determine type
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Post by {self.user.username} ({self.media_type})"


class Story(BaseModel):
    """
    Represents a story uploaded by a user, which expires after 24 hours.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="stories"  # A user can have multiple stories
    )
    media = models.FileField(upload_to='Story/medias/')   # URL of the story image/video
    caption = models.CharField(max_length=255, blank=True, null=True)  # Optional caption
    expires_at = models.DateTimeField(default=lambda: now() + timedelta(hours=24))  # Auto expires in 24 hrs
    media_type = models.CharField(max_length=10, blank=True, null=True)
    is_video = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["-created_at"]),
        ]
        abstract = True
    
    def save(self, *args, **kwargs):
        """ Auto-detect media type based on file extension before saving """
        if self.media:
            self.media_type = validate_file_extension(self.media)  # Determine type
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Story by {self.user.username}"

class Like(BaseModel):
    """
    Represents a 'like' on a post by a user.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="likes"  # A user can like multiple posts
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="likes"  # A post can have multiple likes
    )

    class Meta:
        unique_together = ("user", "post")  # Ensures a user can't like the same post twice
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["post"]),
        ]

    def __str__(self):
        return f"{self.user.username} liked Post {self.post.id}"

class Comment(BaseModel):
    """
    Represents a comment made by a user on a post.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments"  # A user can have multiple comments
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments"  # A post can have multiple comments
    )
    text = models.TextField()  # The content of the comment

    class Meta:
        indexes = [
            models.Index(fields=["post"]),
            models.Index(fields=["user"]),
        ]

    def __str__(self):
        return f"Comment by {self.user.username} on Post {self.post.id}"

class Follower(models.Model):
    """
    Represents a 'follow' relationship between users.
    """
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following"  # User follows multiple people
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="followers"  # User has multiple followers
    )

    class Meta:
        unique_together = ("follower", "following")  # Prevents duplicate follows
        indexes = [
            models.Index(fields=["follower"]),
            models.Index(fields=["following"]),
        ]
        abstract = True

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"



class ChatRoom(BaseModel):
    """
    A chat room between two users.
    """
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chats_as_user1")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chats_as_user2")
    class Meta:
        unique_together = ("user1", "user2")

    def __str__(self):
        return f"Chat: {self.user1.username} & {self.user2.username}"

class Message(BaseModel):
    """
    A message sent between two users in a chat room.
    """
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    content = models.TextField()
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender.username}: {self.content[:20]}"

