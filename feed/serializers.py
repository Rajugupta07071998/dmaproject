from rest_framework import serializers
from .models import *
from account.models import User
from rest_framework.serializers import ValidationError  
import mimetypes
#from mutagen.mp4 import MP4

class LikeSerializer(serializers.ModelSerializer):
    """Serializer for likes"""
    user = serializers.StringRelatedField()

    class Meta:
        model = Like
        fields = ['user', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for comments"""
    user = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ['user', 'text', 'created_at']


def validate_file_extension(value):
    """ Validate if the uploaded file is an image or video based on extension """
    image_extensions = ['jpg', 'jpeg', 'png', 'gif', 'webp']
    video_extensions = ['mp4', 'avi', 'mov', 'mpeg', 'mkv', 'webm']

    ext = value.name.split('.')[-1].lower()  

    if ext in image_extensions:
        return 'image', ext
    elif ext in video_extensions:
        return 'video', ext
    else:
        raise ValidationError("Unsupported file format! Only images and videos are allowed.")


def validate_video_size(media):
    """Ensures video file size is within 3MB and returns JSON error if exceeded."""
    max_size = 15 * 1024 * 1024  # 3MB limit
    if media.size > max_size:
        raise ValidationError({"error": "File size must be less than 3MB."})  # JSON error response
    return round(media.size / (1024 * 1024), 2)  # MB
    
# def validate_video_duration(media):
#     """Check if video duration is between 30 to 90 seconds."""
#     try:
#         video = MP4(media.file)  
#         duration = video.info.length  

#         if duration < 300 or duration > 900:
#             raise ValidationError("Video duration must be between 30 and 90 seconds.")

#     except Exception:
#         raise ValidationError("Could not determine video duration. Ensure it's a valid MP4 file.")

class PostSerializer(serializers.ModelSerializer):
    """Post model ke liye serializer"""
    user = serializers.StringRelatedField()
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    likes = LikeSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    media_url = serializers.SerializerMethodField()  # Add media URL field

    
    class Meta:
        model = Post
        fields = [
            'id', 'user', 'media', 'media_url', 'caption', 'hashtags', 
            'views_count', 'media_type', 'is_video', 'created_at', 
            'likes_count', 'comments_count', 'likes', 'comments'
        ]

    def validate_media(self, media):
        """ Validate file extension and set media type """
        media_type, extension = validate_file_extension(media)  # Determine type
        
        # Automatically assign media type in validated data
        self.extension = extension
        self.media_type = media_type
        self.is_video = media_type == "video"

        self.video_size = validate_video_size(media)
        #validate_video_duration(media)

        return media

    def create(self, validated_data):
        """ Custom create method to set media_type before saving """
        validated_data['extension'] = self.extension
        validated_data['media_type'] = self.media_type
        validated_data['is_video'] = self.is_video
        validated_data['video_size'] = self.video_size
        return super().create(validated_data)

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()
    
    def get_media_url(self, obj):
        return obj.media.url if obj.media else None  # Return the full URL to the media file



class FollowerSerializer(serializers.ModelSerializer):
    follower_username = serializers.CharField(source="follower.username", read_only=True)
    following_username = serializers.CharField(source="following.username", read_only=True)
    follower_full_name = serializers.SerializerMethodField()
    following_full_name = serializers.SerializerMethodField()
    follower_profile_pic = serializers.ImageField(source="follower.personalinfo.profile_pic", read_only=True)
    following_profile_pic = serializers.ImageField(source="following.personalinfo.profile_pic", read_only=True)

    class Meta:
        model = Follower
        fields = [
            "id",
            "follower", "follower_username", "follower_full_name", "follower_profile_pic",
            "following", "following_username", "following_full_name", "following_profile_pic",
        ]

    def get_follower_full_name(self, obj):
        return obj.follower.get_full_name()

    def get_following_full_name(self, obj):
        return obj.following.get_full_name()



class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "email", "followers_count", "following_count"]

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()


class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = "__all__"

class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source="sender.username", read_only=True)

    class Meta:
        model = Message
        fields = ["id", "sender", "sender_username", "content", "is_read", "created_at"]
