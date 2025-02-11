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
 
]
