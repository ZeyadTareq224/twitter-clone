from django import contrib
from django.shortcuts import render, redirect
from django.db.models import Q
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse
from django.urls.base import reverse_lazy
from django.views import View
from django.views.generic.edit import DeleteView, UpdateView
from django.contrib import messages

# Mixins
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Models AND Forms
from core.models import User
from .models import Image, Post, Comment, UserProfile, Thread, Message
from .forms import PostForm, CommentForm, ProfileUpdateForm, ThreadForm, MessageForm, ShareForm
from notifications.models import Notification


class PostListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.filter(author__profile__followers__in=[request.user.id])
        form = PostForm()
        share_form = ShareForm()
        context = {
            'post_list': posts,
            'form': form,
            'shareform': share_form
        }

        return render(request, 'social/post_list.html', context)

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST, request.FILES)
        files = request.FILES.getlist('image')

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            new_post.create_tags()
            

            # saving the uoloaded images to the newly created post
            for f in files:
                img = Image(image=f)
                img.save()
                new_post.image.add(img)
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
            new_comment.create_tags()


            notification = Notification.objects.create(notification_type=2, from_user=request.user, to_user=post.author, post=post)

            messages.success(request, "Thanks for your feedback")
            return redirect('post_detail', pk)
        else:
            messages.error(request, "Something went wrong")
            return redirect('post_detail', pk)
    


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Post
    form_class = PostForm
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


class CommentReplyView(LoginRequiredMixin, View):
    def post(self, request, post_id, comment_id, *args, **kwargs):
        post = Post.objects.get(id=post_id)
        parent_comment = Comment.objects.get(id=comment_id)

        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.parent = parent_comment
            new_comment.save()

            notification = Notification.objects.create(notification_type=2, from_user=request.user, to_user=parent_comment.author, comment=new_comment)

        return redirect('post_detail', pk=post_id)

class ProfileView(View):
    def get(self, request, profile_id, *args, **kwargs):
        profile = UserProfile.objects.get(id=profile_id)
        user = profile.user
        posts = Post.objects.filter(author=user)
        followers = profile.get_followers()
        followers_count = profile.get_followers_count()

        if followers_count == 0:
            is_following = False
        else:
            for follower in followers:
                if follower == request.user:
                    is_following = True
                    break
                else:
                    is_following = False    
        
        context = {
            'posts': posts,
            'user': user,
            'profile': profile,
            'is_following': is_following,
            'followers_count': followers_count,
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


class AddFollower(LoginRequiredMixin , View):
    def post(self, request, profile_id, *args, **kwargs):
        profile = UserProfile.objects.get(id=profile_id)
        profile.followers.add(request.user)
        notification = Notification.objects.create(notification_type=2, from_user=request.user, to_user=profile.user)

        messages.success(request, f"You Followed @{profile.user.username}")
        return redirect('profile', profile_id)


class RemoveFollower(LoginRequiredMixin, View):
    def post(self, request, profile_id, *args, **kwargs):
        profile = UserProfile.objects.get(id=profile_id)
        profile.followers.remove(request.user)
        messages.success(request, f"You Unfollowed @{profile.user.username}")
        return redirect('profile', profile_id)


class AddLike(LoginRequiredMixin, View):
    def post(self, request, post_id, *args, **kwargs):
        post = Post.objects.get(id=post_id)

        # check if the user already disliked the post
        is_dislike = False
        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break
        
        # check if the user already disliked the post:- remove the dislike before adding like
        if is_dislike:
            post.dislikes.remove(request.user)

        # check if the user already liked the post
        is_like = False
        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break
        
        if not is_like:
            post.likes.add(request.user)
            notification = Notification.objects.create(notification_type=1, from_user=request.user, to_user=post.author, post=post)


        if is_like:
            post.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

class AddDislike(LoginRequiredMixin, View):
    def post(self, request, post_id, *args, **kwargs):
        post = Post.objects.get(id=post_id)

        # check if the user already liked the post
        is_like = False
        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break
        
        # check if the user already liked the post:- remove the like before adding dislike
        if is_like:
            post.likes.remove(request.user)


        # check if the user already disliked the post
        is_dislike = False
        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break
        
        if not is_dislike:
            post.dislikes.add(request.user)

        if is_dislike:
            post.dislikes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)



class AddCommentLike(LoginRequiredMixin, View):
    def post(self, request, comment_id, *args, **kwargs):
        comment = Comment.objects.get(id=comment_id)

        is_dislike = False

        for dislike in comment.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if is_dislike:
            comment.dislikes.remove(request.user)

        is_like = False

        for like in comment.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            comment.likes.add(request.user)
            notification = Notification.objects.create(notification_type=1, from_user=request.user, to_user=comment.author, comment=comment)

        if is_like:
            comment.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

class AddCommentDislike(LoginRequiredMixin, View):
    def post(self, request, comment_id, *args, **kwargs):
        comment = Comment.objects.get(id=comment_id)

        is_like = False

        for like in comment.likes.all():
            if like == request.user:
                is_like = True
                break

        if is_like:
            comment.likes.remove(request.user)

        is_dislike = False

        for dislike in comment.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if not is_dislike:
            comment.dislikes.add(request.user)

        if is_dislike:
            comment.dislikes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)



class SharePostView(View):
    def post(self, request, post_id, *args, **kwargs):
        original_post = Post.objects.get(id=post_id)
        form = ShareForm(request.POST)
        if form.is_valid():
            new_post = Post(
                shared_body=self.request.POST.get('body'),
                body = original_post.body,
                author = original_post.author,
                created_at = original_post.created_at,
                shared_user = request.user,
                shared_at = timezone.now(),
            )
            new_post.save()

            for img in original_post.image.all():
                new_post.image.add(img)
            new_post.save()    
        return redirect('post_list')


class UserSeaerch(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('query', None)
        profile_list = UserProfile.objects.filter(Q(user__username__icontains=query))

        context = {
            'profile_list': profile_list,
        }
        return render(request, 'social/search.html', context)


class FollowersListView(View):
    def get(self, request, profile_id, *args, **kwargs):
        profile = UserProfile.objects.get(id=profile_id)
        followers = profile.get_followers()

        context = {
            'profile': profile, 
            'followers': followers
        }

        return render(request, 'social/followers_list.html', context)


class PostNotification(View):
    def get(self, request, notification_id, post_id, *args, **kwargs):
        notification = Notification.objects.get(id=notification_id)
        

        notification.user_has_seen = True
        notification.save()

        return redirect('post_detail', post_id)


class FollowNotification(View):
    def get(self, request, notification_id, profile_id, *args, **kwargs):
        notification = Notification.objects.get(id=notification_id)
        

        notification.user_has_seen = True
        notification.save()

        return redirect('profile', profile_id)


class ThreadNotification(View):
    def get(self, request, notification_id, thread_id, *args, **kwargs):
        notification = Notification.objects.get(id=notification_id)

        notification.user_has_seen = True
        notification.save()
        return redirect('thread', thread_id)


class FriendRequestNotification(View):
    def get(self, request, notification_id, profile_id, *args, **kwargs):
        notification = Notification.objects.get(id=notification_id)
        notification.user_has_seen = True
        notification.save()
        return redirect('profile', profile_id) # TODO CHANGE THIS

class RemoveNotification(View):
    def delete(self, request, notification_id, *args, **kwargs):
        notification = Notification.objects.get(id=notification_id)
        notification.user_has_seen = True
        notification.save()
        return HttpResponse('Success', content_type='text/plain')



class ListThreads(View):
    def get(self, request, *args, **kwargs):
        threads = Thread.objects.filter(Q(user=request.user) | Q(receiver=request.user))

        context = {
            'threads': threads
        }
        return render(request, 'social/inbox.html', context)


class CreateThread(View):
    def get(self, request, *args, **kwargs):
        form = ThreadForm()

        context = {
            'form': form
        }
        return render(request, 'social/create_thread.html', context)

    def post(self, request, *args, **kwargs):
        form = ThreadForm(request.POST)
        username = request.POST.get('username')
        try:
            receiver = User.objects.get(username=username)

            if Thread.objects.filter(user=request.user, receiver=receiver).exists():
                thread = Thread.objects.filter(user=request.user, receiver=receiver)[0]
                return redirect('thread', thread.id)

            elif Thread.objects.filter(user=receiver, receiver=request.user).exists():
                thread = Thread.objects.filter(user=receiver, receiver=request.user)[0]
                return redirect('thread', thread.id)

            if form.is_valid():
                thread = Thread(user = request.user, receiver=receiver)
                thread.save()
                return redirect('thread', thread.id)
        except:
            messages.error(request, 'Invalid username')
            return redirect('create_thread')
            
class ThreadView(View):
    def get(self, request, thread_id, *args, **kwargs):
        form = MessageForm()
        thread = Thread.objects.get(id=thread_id)
        messages_list = Message.objects.filter(thread=thread)
        context = {
            'form': form,
            'thread': thread,
            'messages_list': messages_list
        }
        return render(request, 'social/thread.html', context)


class CreateMessage(View):
    def post(self, request, thread_id, *args, **kwargs):
        thread = Thread.objects.get(id=thread_id)
        if thread.receiver == request.user:
            receiver = thread.user
        else:
            receiver = thread.receiver

        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.thread = thread
            message.sender_user = request.user
            message.receiver_user = receiver
            message.save()
            
        
        Notification.objects.create(notification_type=4, from_user=request.user, to_user=receiver, thread=thread)
        return redirect('thread', thread_id)


class AddFriend(View):
    def post(self, request, profile_id, *args, **kwargs):
        profile = UserProfile.objects.get(id=profile_id)
        if request.user != profile.user:
            profile.friend_requests.add(request.user)
            profile.save()
            receiver = profile.user
            Notification.objects.create(notification_type=5, from_user=request.user, to_user=receiver)
            messages.success(request, 'Friend request sent successfully')
            return redirect('profile', profile_id)


class CancelFriendRequest(View):
    def post(self, request, profile_id, *args, **kwargs):
        profile = UserProfile.objects.get(id=profile_id)
        profile.friend_requests.remove(request.user)
        profile.save()
        messages.success(request, 'Friend request canceled successfully')
        return redirect('profile', profile_id)