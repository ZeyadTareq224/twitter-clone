from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

from .models import Post
from .forms import PostForm, CommentForm


class PostListView(View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        form = PostForm()

        context = {
            'post_list': posts,
            'form': form,
        }

        return render(request, 'social/post_list.html', context)

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            messages.success(request, "Your post added successfully")
            return redirect('post_list')
        else:
            messages.error(request, 'Something went worng')
            return redirect('post_list')

class PostDetailView(View):
    def get(slef, request, pk, *args, **kwargs):
        post = Post.objects.get(id=pk)
        form = CommentForm()

        context = {
            'post': post,
            'form': form,
        }

        return render(request, 'social/post_detail.html', context)

    def post(self, request, *args, **kwargs):
        pass