from rest_framework import serializers
from .models import *
from account.models import User

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
        fields = ['id', 'user', 'media', 'media_url', 'caption', 'hashtags', 'views_count', 'media_type', 'is_video', 'created_at', 'likes_count', 'comments_count', 'likes', 'comments']

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
