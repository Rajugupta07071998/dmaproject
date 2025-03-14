from rest_framework import serializers
from .models import *

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
