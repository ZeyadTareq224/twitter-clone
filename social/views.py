from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls.base import reverse_lazy
from django.views import View
from django.views.generic.edit import DeleteView, UpdateView
from django.contrib import messages

# Mixins
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Models AND Forms
from .models import Post, Comment, UserProfile
from .forms import PostForm, CommentForm, ProfileUpdateForm


class PostListView(LoginRequiredMixin, View):
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

class PostDetailView(LoginRequiredMixin, View):
    def get(slef, request, pk, *args, **kwargs):
        post = Post.objects.get(id=pk)
        form = CommentForm()
        comments = Comment.objects.filter(post=post)

        context = {
            'post': post,
            'form': form,
            'comments': comments,
        }
        
        return render(request, 'social/post_detail.html', context)

    def post(self,request, pk, *args, **kwargs):
        post = Post.objects.get(id=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()
            messages.success(request, "Thanks for your feedback")
            return redirect('post_detail', pk)
        else:
            messages.error(request, "Something went wrong")
            return redirect('post_detail', pk)
    




class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Post
    fields = ['body']
    template_name = 'social/post_edit.html' 
    success_message = "Post updated"

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Post
    template_name = 'social/post_delete.html'
    success_message = "Post deleted"

    def get_success_url(self):
        return reverse_lazy('post_list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(PostDeleteView, self).delete(request, *args, **kwargs)    


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Comment
    template_name = 'social/comment_delete.html'
    success_message = "Comment deleted"

    def get_success_url(self):
        post_pk = self.kwargs['post_pk']
        return reverse_lazy('post_detail', kwargs={'pk': post_pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(CommentDeleteView, self).delete(request, *args, **kwargs)


class ProfileView(View):
    def get(self, request, profile_id, *args, **kwargs):
        profile = UserProfile.objects.get(id=profile_id)
        user = profile.user
        posts = Post.objects.filter(author=user)

        context = {
            'posts': posts,
            'user': user,
            'profile': profile,
        }
        return render(request, 'social/profile.html', context)


class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = UserProfile
    template_name = 'social/profile_update.html'
    form_class = ProfileUpdateForm


    def get_success_url(self):
        profile_id = self.kwargs['pk']
        return reverse_lazy('profile', kwargs={'profile_id': profile_id})


    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user    