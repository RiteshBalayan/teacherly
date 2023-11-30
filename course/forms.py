from django import forms
from .models import Course, Chapter, Page

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [ 'title', 'thumbnail', 'description', 'topics']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full py-4 px-6 rounded-xl', 'placeholder': 'title'}),            
            'thumbnail': forms.FileInput(attrs={'class': 'w-full py-4 px-6 rounded-xl'}),
            'description': forms.TextInput(attrs={'class': 'w-full py-4 px-6 rounded-xl', 'placeholder': 'description'}),
            'topics': forms.SelectMultiple(attrs={'class': 'w-full py-4 px-6 rounded-xl'}),
        }
class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['title']

class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['title']

from content.models import Video, Image, Article

class VideoFormCourse(forms.ModelForm):
    class Meta:
        model = Video
        fields = [ 'title', 'video_file', 'explanation','bitesizable']

class ImageFormCourse(forms.ModelForm):
    class Meta:
        model = Image
        fields = [ 'title', 'image_file', 'explanation','bitesizable']
        


class ArticleFormCourse(forms.ModelForm):
    class Meta:
        model = Article
        fields = [ 'title', 'content','bitesizable']