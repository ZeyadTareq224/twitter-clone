from django import forms
from .models import Post, Comment, UserProfile


class PostForm(forms.ModelForm):
    body = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows': '3',
            'placeholder': 'Say Something...'
        })
    )

    image = forms.ImageField(required=False, label='')
    
    class Meta:
        model = Post
        fields = ['body', 'image']
        


class CommentForm(forms.ModelForm):
    comment = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={'rows': '3',
                   'placeholder': 'Say Something...'}
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
    