from django.urls import path
from .views import *  



urlpatterns = [
    # Post 
    path('posts/list/', PostListAPIView.as_view(), name='post-list'), 
    path('posts/list/user/', PostListUserAPIView.as_view(), name='post-list-user'),
    path('posts/create/', PostCreateUpdateDeleteAPIView.as_view(), name='post-create'),  # To upload a post
    path('posts/update/<pk>/', PostCreateUpdateDeleteAPIView.as_view(), name='post-update'),  # To update a post by pk
    path('posts/delete/<pk>/', PostCreateUpdateDeleteAPIView.as_view(), name='post-delete'),

    # Like and comment
    path('posts/<post_id>/like/', LikePostAPIView.as_view(), name='post-like'),  # Like/unlike a post
    path('posts/<post_id>/comment/', CommentPostAPIView.as_view(), name='post-comment'),  # Add a comment

    path("search-users/", UserSearchAPIView.as_view(), name="user-search"),
    path('follow/<uuid:user_id>/', FollowUserAPIView.as_view(), name='follow-user'),
    path('unfollow/<uuid:user_id>/', UnfollowUserAPIView.as_view(), name='unfollow-user'),
    path('followers/<uuid:user_id>/', FollowerListAPIView.as_view(), name='followers-list'),
    path('following/<uuid:user_id>/', FollowingListAPIView.as_view(), name='following-list'),
    path("user/<uuid:user_id>/", UserProfileAPIView.as_view(), name="user-profile"),
    path('follow-status/<uuid:user_id>/', CheckFollowStatusAPIView.as_view(), name='follow-status'),
    path('suggested-users/', SuggestedUsersAPIView.as_view(), name='suggested-users'),

    path("chats/", ChatListAPIView.as_view(), name="chat-list"),
    path("chats/<room_id>/messages/", ChatMessagesAPIView.as_view(), name="chat-messages"),
    path("chats/<room_id>/send-message/", SendMessageAPIView.as_view(), name="send-message"),
    path('chats/create/<user2_id>/', CreateChatRoomAPIView.as_view(), name='create-chat-room'),
 
]
