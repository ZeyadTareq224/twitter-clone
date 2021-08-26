from django.conf.urls import url
from django.urls import path
from .views import PostListView, PostDetailView

urlpatterns = [
    path('', PostListView.as_view(), name="post_list"),
    path('post/<str:pk>/', PostDetailView.as_view(), name="post_detail"),
]


