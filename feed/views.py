#from urllib import request
from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from .models import Post
from .serializers import PostSerializer, FollowerSerializer, UserSerializer, ChatRoomSerializer, MessageSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from account.models import User
from .models import *
from core.models import *
from rest_framework import permissions



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



from django.db.models import Q

class UserSearchAPIView(APIView):
    """
    Search users globally by username, full name, business name, or business type.
    """

    def get(self, request):
        query = request.GET.get("q", "").strip()
        
        if not query:
            return Response({"error": "Search query is required."}, status=status.HTTP_400_BAD_REQUEST)

        users = User.objects.filter(
            Q(username__icontains=query) | 
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query) | 
            Q(businessinfo__business_name__icontains=query) |  # Search in business name
            Q(businessinfo__business_type__icontains=query)  # Search in business type
        ).distinct()[:10]  # Limit results to 10

        user_data = []
        for user in users:
            user_info = {
                "id": user.id,
                "username": user.username,
                "full_name": user.get_full_name(),
                "profile_pic": user.personalinfo.profile_pic.url if hasattr(user, "personalinfo") and user.personalinfo.profile_pic else None,
                "user_type": user.user_type,
            }

            # If the user is a business, add business details
            if user.user_type == "business" and hasattr(user, "businessinfo"):
                user_info["business_details"] = {
                    "business_name": user.businessinfo.business_name,
                    "business_type": user.businessinfo.get_business_type_display(),
                    "business_logo": user.businessinfo.business_logo.url if user.businessinfo.business_logo else None
                }

            user_data.append(user_info)

        return Response(user_data, status=status.HTTP_200_OK)



class FollowUserAPIView(APIView):
    """
    Follow a user (like Instagram).
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        follower = request.user
        try:
            following = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        if follower == following:
            return Response({"error": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        obj, created = Follower.objects.get_or_create(follower=follower, following=following)
        if created:
            return Response({"message": "You are now following this user."}, status=status.HTTP_201_CREATED)
        return Response({"message": "You are already following this user."}, status=status.HTTP_200_OK)


class UnfollowUserAPIView(APIView):
    """
    Unfollow a user (like Instagram).
    """
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, user_id):
        follower = request.user
        try:
            following = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        deleted, _ = Follower.objects.filter(follower=follower, following=following).delete()
        if deleted:
            return Response({"message": "You have unfollowed this user."}, status=status.HTTP_200_OK)
        return Response({"error": "You are not following this user."}, status=status.HTTP_400_BAD_REQUEST)


class FollowerListAPIView(APIView):
    """
    Get followers of a user (Instagram-style).
    """

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        followers = user.followers.all().select_related("follower__personalinfo")  # Optimized DB query
        count = followers.count()

        follower_list = [
            {
                "id": follower.follower.id,
                "username": follower.follower.username,
                "full_name": follower.follower.get_full_name(),
                "profile_pic": follower.follower.personalinfo.profile_pic.url if follower.follower.personalinfo.profile_pic else None,
                #"is_private": follower.follower.is_private  # Show if user is private
            }
            for follower in followers
        ]

        return Response({"followers_count": count, "followers": follower_list}, status=status.HTTP_200_OK)


class FollowingListAPIView(APIView):
    """
    Get list of users a user is following (Instagram-style).
    """

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        following = user.following.all().select_related("following__personalinfo")  # Optimized DB query
        count = following.count()

        following_list = [
            {
                "id": follow.following.id,
                "username": follow.following.username,
                "full_name": follow.following.get_full_name(),
                "profile_pic": follow.following.personalinfo.profile_pic.url if follow.following.personalinfo.profile_pic else None
            }
            for follow in following
        ]

        return Response({"following_count": count, "following": following_list}, status=status.HTTP_200_OK)


class UserProfileAPIView(APIView):
    """
    Fetch user profile details along with follower count, following count, business details,
    and the list of posts uploaded by the user.
    """

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        viewer = request.user if request.user.is_authenticated else None

        # Check if the account is private and if the viewer is not a follower
        is_private = user.is_private
        is_follower = user.followers.filter(follower=viewer).exists() if viewer else False


        # Get follower and following count
        follower_count = user.followers.count()
        following_count = user.following.count()

        # Default response for personal users
        user_data = {
            "id": user.id,
            "username": user.username,
            "full_name": user.get_full_name(),
            "profile_pic": user.personalinfo.profile_pic.url if hasattr(user, 'personalinfo') and user.personalinfo.profile_pic else None,
            "user_type": user.user_type,
            "follower_count": follower_count,
            "following_count": following_count
        }

        # If the user is a business, add business details
        if user.user_type == "business":
            try:
                business = user.businessinfo
                user_data["business_details"] = {
                    "business_name": business.business_name,
                    "business_type": business.get_business_type_display(),
                    "business_owner": business.business_owner,
                    "business_about": business.business_about,
                    "business_address": business.business_address,
                    "business_phone": business.business_phone,
                    "business_email": business.business_email,
                    "business_website": business.business_website,
                    "established_year": business.established_year,
                    "number_of_employees": business.number_of_employees,
                    "business_logo": business.business_logo.url if business.business_logo else None,
                }
            except BusinessInfo.DoesNotExist:
                user_data["business_details"] = None  # No business info found

        # If account is private and viewer is not a follower, hide posts
        if is_private and not is_follower and viewer != user:
            user_data["posts"] = "This account is private. Follow to see posts."
        else:
            posts = user.posts.all().order_by("-created_at")[:10]
            user_data["posts"] = [
                {
                    "id": post.id,
                    "media_url": post.media.url if post.media else None,
                    "caption": post.caption,
                    "hashtags": post.hashtags,
                    "views_count": post.views_count,
                    "media_type": post.media_type,
                    "is_video": post.is_video
                }
                for post in posts
            ]

        return Response(user_data, status=status.HTTP_200_OK)


class CheckFollowStatusAPIView(APIView):
    """
    Check if a user is following another user.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id):
        follower = request.user
        try:
            following = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        is_following = Follower.objects.filter(follower=follower, following=following).exists()
        return Response({"is_following": is_following}, status=status.HTTP_200_OK)


class SuggestedUsersAPIView(APIView):
    """
    Suggest users to follow with profile details.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        following_users = user.following.values_list('following', flat=True)

        # Exclude users already followed & self
        suggested_users = User.objects.exclude(id__in=following_users).exclude(id=user.id).order_by("?")[:5]

        # Prepare response data with full user details
        suggested_users_data = [
            {
                "id": suggested_user.id,
                "username": suggested_user.username,
                "full_name": suggested_user.get_full_name(),
                "profile_pic": suggested_user.personalinfo.profile_pic.url if hasattr(suggested_user, "personalinfo") and suggested_user.personalinfo.profile_pic else None
            }
            for suggested_user in suggested_users
        ]

        return Response(suggested_users_data, status=status.HTTP_200_OK)



class ChatListAPIView(APIView):
    def get(self, request):
        user = request.user
        chats = ChatRoom.objects.filter(user1=user) | ChatRoom.objects.filter(user2=user)
        serializer = ChatRoomSerializer(chats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ChatMessagesAPIView(APIView):
    def get(self, request, room_id):
        try:
            chat_room = ChatRoom.objects.get(id=room_id)
        except ChatRoom.DoesNotExist:
            return Response({"error": "Chat room not found"}, status=status.HTTP_404_NOT_FOUND)

        messages = chat_room.messages.all().order_by("created_at")
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SendMessageAPIView(APIView):
    def post(self, request, room_id):
        try:
            chat_room = ChatRoom.objects.get(id=room_id)
        except ChatRoom.DoesNotExist:
            return Response({"error": "Chat room not found"}, status=status.HTTP_404_NOT_FOUND)

        sender = request.user
        content = request.data.get("content")

        if not content:
            return Response({"error": "Message cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)

        message = Message.objects.create(chat_room=chat_room, sender=sender, content=content)
        return Response({"message": "Message sent successfully"}, status=status.HTTP_201_CREATED)



class CreateChatRoomAPIView(APIView):
    """
    Creates a new chat room if it doesn't exist.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user2_id):
        user1 = request.user  # Current logged-in user

        try:
            user2 = User.objects.get(id=user2_id)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        if user1 == user2:
            return Response({"error": "You cannot chat with yourself."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if chat room already exists
        chat_room, created = ChatRoom.objects.get_or_create(user1=user1, user2=user2)
        
        return Response({
            "chat_room_id": chat_room.id,
            "user1": user1.username,
            "user2": user2.username,
            "created": created
        }, status=status.HTTP_201_CREATED)