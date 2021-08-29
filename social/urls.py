from django.conf.urls import url
from django.urls import path
from .views import AddDislike, AddFollower, AddLike, CommentDeleteView, PostListView, PostDetailView, PostUpdateView, PostDeleteView, ProfileUpdateView, ProfileView, RemoveFollower, UserSeaerch

urlpatterns = [
    path('', PostListView.as_view(), name="post_list"),
    path('post/<int:pk>/', PostDetailView.as_view(), name="post_detail"),
    path('post/update/<int:pk>/', PostUpdateView.as_view(), name="post_update"),
    path('post/delete/<int:pk>/', PostDeleteView.as_view(), name="post_delete"),
    path('post/<int:post_pk>/comment/delete/<int:pk>/', CommentDeleteView.as_view(), name="comment_delete"),
    path('post/<int:post_id>/like/', AddLike.as_view(), name="like"),
    path('post/<int:post_id>/dislike/', AddDislike.as_view(), name="dislike"),
    

    path('profile/<int:profile_id>/', ProfileView.as_view(), name="profile"),
    path('profile/update/<int:pk>/', ProfileUpdateView.as_view(), name="profile_update"),
    path('profile/<int:profile_id>/followers/add/', AddFollower.as_view(), name="add_follower"),
    path('profile/<int:profile_id>/followers/remove/', RemoveFollower.as_view(), name="remove_follower"),

    path('search/', UserSeaerch.as_view(), name="profile_search"),
    
]


