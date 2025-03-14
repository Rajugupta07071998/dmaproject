#from urllib import request
from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from .models import Post
from .serializers import PostSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from account.models import User
from .models import *
from core.models import *



class CustomPagination(PageNumberPagination):
    """Posts ke liye pagination class"""
    page_size = 10  # Default: 10 posts per page
    page_size_query_param = 'page_size'  # Client custom page size set kar sakta hai
    max_page_size = 50  # Maximum limit: 50 posts per page


class PostListAPIView(generics.ListAPIView):
    """API for retrieving paginated list of posts by GET"""
    
    queryset = Post.objects.all().order_by('-created_at')  # Latest posts fetch karo
    serializer_class = PostSerializer  # Serializer ka use karo
    pagination_class = CustomPagination  # Custom pagination set karo


class PostListUserAPIView(generics.ListAPIView):
    """API to fetch all posts of a current user by GET"""

    serializer_class = PostSerializer  
    pagination_class = CustomPagination 

    def get_queryset(self):
        """Filter posts by logged-in user"""
        return Post.objects.filter(user=self.request.user).order_by('-created_at')


class PostCreateUpdateDeleteAPIView(APIView):
    """API for uploading a new post by Create, Delete and Partial Update"""

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(user=request.user)  # Automatically assign the current user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        try:
            post = Post.objects.get(pk=pk) 
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Create a serializer with the existing data and new partial data
        serializer = PostSerializer(post, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        try:
            post = Post.objects.get(pk=pk) 
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Ensure only the post owner can delete it
        if post.user != request.user:
            return Response({"error": "You do not have permission to delete this post."}, status=status.HTTP_403_FORBIDDEN)

        post.delete()
        return Response({"message": "Post deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class LikePostAPIView(APIView):
    """API for liking/unliking a post"""

    def post(self, request, post_id):
        try:
            post = Post.objects.get(pk=post_id) 
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            like.delete()  # Unlike if already liked
            return Response({"message": "Unliked the post"}, status=status.HTTP_200_OK)
        
        create_feed_notification(request.user, post, 'post_like', f"{request.user.username} liked your post.")

        return Response({"message": "Liked the post"}, status=status.HTTP_201_CREATED)
    


class CommentPostAPIView(APIView):
    """API for adding a comment on a post"""

    def post(self, request, post_id):
        try:
            post = Post.objects.get(pk=post_id) 
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        text = request.data.get("text")

        if not text:
            return Response({"error": "Comment cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)

        comment = Comment.objects.create(user=request.user, post=post, text=text)

        create_feed_notification(request.user, post, 'post_comment', f"{request.user.username} commented: {text[:30]}")

        return Response({"message": "Comment added", "comment": comment.text}, status=status.HTTP_201_CREATED)
