from django.db import models

# Create your models here.

from django.utils.timezone import now
from datetime import timedelta
from account.models import User
from core.models import BaseModel

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
    media = models.FileField(upload_to='Post/medias/')  # This will now upload to S3
    caption = models.TextField(blank=True, null=True)  # Caption text
    hashtags = models.CharField(max_length=500, blank=True, null=True)  # List of hashtags (stored as JSON)
    views_count = models.PositiveBigIntegerField(default=0)  # Number of views (scaled)

    class Meta:
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["-created_at"]),
        ]

    def __str__(self):
        return f"Post by {self.user.username}"


class Story(BaseModel):
    """
    Represents a story uploaded by a user, which expires after 24 hours.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="stories"  # A user can have multiple stories
    )
    media_url = models.URLField()  # URL of the story image/video
    caption = models.CharField(max_length=255, blank=True, null=True)  # Optional caption
    expires_at = models.DateTimeField(default=lambda: now() + timedelta(hours=24))  # Auto expires in 24 hrs

    class Meta:
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["-created_at"]),
        ]
        abstract = True

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



