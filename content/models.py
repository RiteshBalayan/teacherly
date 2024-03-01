from django.db import models
from django.contrib.auth.models import User
from course.models import Page
from core.models import Likable, Commentable, Endorsable, VideoCommentable, Savable
from embed_video.fields import EmbedVideoField

class URLVideo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE )
    title = models.CharField(max_length=200)
    video_url = EmbedVideoField()  
    explanation = models.TextField(blank=True)
    course = models.ForeignKey(Page, on_delete=models.SET_NULL, null=True, blank=True, related_name='URLVideo')

    def __str__(self):
        return self.title


class Video(Likable, Commentable, Savable):
    user = models.ForeignKey(User, on_delete=models.CASCADE )
    title = models.CharField(max_length=100)
    video_file = models.FileField(upload_to='video_files/', blank=True)
    explanation = models.TextField(blank=True)
    course = models.ForeignKey(Page, on_delete=models.SET_NULL, null=True, blank=True, related_name='videos')
    bitesizable = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Image(Likable, Commentable, Savable):
    user = models.ForeignKey(User, on_delete=models.CASCADE )
    title = models.CharField(max_length=100)
    image_file = models.FileField(upload_to='image_files/')  # FileField for image files
    explanation = models.TextField( blank=True)
    course = models.ForeignKey(Page, on_delete=models.SET_NULL, null=True, blank=True, related_name='images')
    bitesizable = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Article(Likable, Commentable, Savable):
    user = models.ForeignKey(User, on_delete=models.CASCADE )
    title = models.CharField(max_length=100)
    content = models.TextField()
    course = models.ForeignKey(Page, on_delete=models.SET_NULL, null=True, blank=True, related_name='articles')
    bitesizable = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Question(Likable, Commentable, Endorsable, VideoCommentable, Savable):
    user = models.ForeignKey(User, on_delete=models.CASCADE )
    title = models.CharField(max_length=100, blank=True)
    question_text = models.TextField()
    explanation = models.TextField(blank=True, null=True)
    course = models.ForeignKey(Page, on_delete=models.SET_NULL, null=True, blank=True, related_name='questions')
    bitesizable = models.BooleanField(default=False)

    def __str__(self):
        return self.question_text

class QuestionOption(models.Model):
    Options = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    option_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.option_text
