from .models import  Video, Article, Image, Question, QuestionOption
from django.contrib import admin
from core.models import Like, Likable, Comment, Commentable, Endorse, VideoComment, Endorsable, VideoCommentable, Save, Savable
from django.contrib.contenttypes.admin import GenericTabularInline

# Define a generic inline for comments
class CommentInline(GenericTabularInline):
    model = Comment
    extra = 1

# Define a generic inline for likes
class LikeInline(GenericTabularInline):
    model = Like
    extra = 1

# Define a generic inline for endorse
class EndorseInline(GenericTabularInline):
    model = Endorse
    extra = 1

# Define a generic inline for video comment
class VideoCommentInline(GenericTabularInline):
    model = VideoComment
    extra = 1

# Define a generic inline for save
class SaveInline(GenericTabularInline):
    model = Save
    extra = 1

class QuestionOptionInline(admin.TabularInline):
    model = QuestionOption
    extra = 1

# Register your models here.
@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'video_file')
    inlines = [CommentInline, LikeInline, SaveInline]

# Register your models here.
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    inlines = [CommentInline, LikeInline, SaveInline]

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title',)
    inlines = [CommentInline, LikeInline, SaveInline]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [QuestionOptionInline, CommentInline, LikeInline, EndorseInline, VideoCommentInline, SaveInline]

admin.site.register(QuestionOption)
