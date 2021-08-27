from django.conf.urls import url
from django.urls import path
from .views import CommentDeleteView, PostListView, PostDetailView, PostUpdateView, PostDeleteView

urlpatterns = [
    path('', PostListView.as_view(), name="post_list"),
    path('post/<int:pk>/', PostDetailView.as_view(), name="post_detail"),
    path('post/update/<int:pk>/', PostUpdateView.as_view(), name="post_update"),
    path('post/delete/<int:pk>/', PostDeleteView.as_view(), name="post_delete"),
    path('post/<int:post_pk>/comment/delete/<int:pk>/', CommentDeleteView.as_view(), name="comment_delete"),
]


