from django import forms
from .models import Video, Image, Article, Question, QuestionOption

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = [ 'title', 'video_file', 'explanation']

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = [ 'title', 'image_file', 'explanation']
        


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [ 'title', 'content']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'question_text', 'explanation']

class QuestionOptionForm(forms.ModelForm):
    class Meta:
        model = QuestionOption
        fields = ['option_text', 'is_correct']

