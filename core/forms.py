from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Comment, Profile, VideoComment

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'Your email address',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Repeat password',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment'] 

class VideoCommentForm(forms.ModelForm):
    class Meta:
        model = VideoComment
        fields = ['comment']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['description', 'profile_pic']
        widgets = {
            'description': forms.TextInput(attrs={'class': 'w-full py-4 px-6 rounded-xl', 'placeholder': 'Description'}),
            'profile_pic': forms.FileInput(attrs={'class': 'w-full py-4 px-6 rounded-xl'}),
        }