from django.conf.urls import url
from django.urls import path
from .views import AddFollower, CommentDeleteView, PostListView, PostDetailView, PostUpdateView, PostDeleteView, ProfileUpdateView, ProfileView, RemoveFollower

urlpatterns = [
    path('', PostListView.as_view(), name="post_list"),
    path('post/<int:pk>/', PostDetailView.as_view(), name="post_detail"),
    path('post/update/<int:pk>/', PostUpdateView.as_view(), name="post_update"),
    path('post/delete/<int:pk>/', PostDeleteView.as_view(), name="post_delete"),
    path('post/<int:post_pk>/comment/delete/<int:pk>/', CommentDeleteView.as_view(), name="comment_delete"),
    path('profile/<int:profile_id>/', ProfileView.as_view(), name="profile"),
    path('profile/update/<int:pk>/', ProfileUpdateView.as_view(), name="profile_update"),
    path('profile/<int:profile_id>/followers/add/', AddFollower.as_view(), name="add_follower"),
    path('profile/<int:profile_id>/followers/remove/', RemoveFollower.as_view(), name="remove_follower"),
]


