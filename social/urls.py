from django.conf.urls import url
from django.urls import path
from .views import PostNotification, FollowNotification, CommentReplyView, AddCommentDislike, AddCommentLike, FollowersListView, AddDislike, AddFollower, AddLike, CommentDeleteView, PostListView, PostDetailView, PostUpdateView, PostDeleteView, ProfileUpdateView, ProfileView, RemoveFollower, RemoveNotification, UserSeaerch

urlpatterns = [
    path('', PostListView.as_view(), name="post_list"),
    path('post/<int:pk>/', PostDetailView.as_view(), name="post_detail"),
    path('post/update/<int:pk>/', PostUpdateView.as_view(), name="post_update"),
    path('post/delete/<int:pk>/', PostDeleteView.as_view(), name="post_delete"),
    path('post/<int:post_pk>/comment/delete/<int:pk>/', CommentDeleteView.as_view(), name="comment_delete"),
    path('post/<int:post_id>/comment/<int:comment_id>/like', AddCommentLike.as_view(), name='comment_like'),
    path('post/<int:post_id>comment/<int:comment_id>/dislike', AddCommentDislike.as_view(), name='comment_dislike'),
    path('post/<int:post_id>/like/', AddLike.as_view(), name="like"),
    path('post/<int:post_id>/dislike/', AddDislike.as_view(), name="dislike"),
    path('post/<int:post_id>/comment/<int:comment_id>/reply/', CommentReplyView.as_view(), name="comment_reply"),

    path('profile/<int:profile_id>/', ProfileView.as_view(), name="profile"),
    path('profile/update/<int:pk>/', ProfileUpdateView.as_view(), name="profile_update"),
    path('profile/<int:profile_id>/followers/add/', AddFollower.as_view(), name="add_follower"),
    path('profile/<int:profile_id>/followers/remove/', RemoveFollower.as_view(), name="remove_follower"),
    path('profile/<int:profile_id>/followers/', FollowersListView.as_view(), name="followers_list"),


    path('search/', UserSeaerch.as_view(), name="profile_search"),
    
    path('notification/<int:notification_id>/post/<int:post_id>/', PostNotification.as_view(), name="post_notification"),
    path('notification/<int:notification_id>/profile/<int:profile_id>/', FollowNotification.as_view(), name="follow_notification"),
    path('notification/delete/<int:notification_id>/', RemoveNotification.as_view(), name="notification_delete"),
    
]


