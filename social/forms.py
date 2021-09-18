from django import forms
from django.db.models import fields
from .models import Message, Post, Comment, UserProfile


class PostForm(forms.ModelForm):
    body = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows': '3',
            'placeholder': 'Say Something...'
        })
    )

    image = forms.ImageField(
        required=False,
        label='',
        widget=forms.ClearableFileInput(attrs={
            'multiple': True
        })
    )
    
    class Meta:
        model = Post
        fields = ['body']
        


class CommentForm(forms.ModelForm):
    comment = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={'rows': '3',
                   'placeholder': 'Comment...'}
        ))

    class Meta:
        model = Comment
        fields = ['comment']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'bio', 'birth_date', 'location', 'picture']
        widgets = {
            'birth_date': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
        }


class ThreadForm(forms.Form):
    username = forms.CharField(max_length=100, label='')


class MessageForm(forms.ModelForm):
    body = forms.CharField(max_length=1000, label='')
    image = forms.ImageField(required=False, label='')

    class Meta:
        model = Message
        fields = ['body', 'image']

