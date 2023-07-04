from django.urls import path

from . import views


urlpatterns = [
    path('posts/',views.CreatePost.as_view(), name='create_post'),
    path('posts/<int:post_id>/', views.CreatePost.as_view(), name='post-detail'),
    path('like_posts/<int:post_id>/', views.LikePostAPIView.as_view(), name='like-post'),
    path('users/<int:user_id>/', views.FollowerListAPIView.as_view(), name='follower-list'),
    path('users/<int:user_id>/', views.FollowerListAPIView.as_view(), name='create_follower'),
    path('users/<int:user_id>/', views.FollowerListAPIView.as_view(), name='unfollow'),
]
