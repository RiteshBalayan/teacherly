from django.contrib import admin
from .models import Topic, Course, Chapter, Page
from core.models import Comment, Commentable, Like, Likable, Save, Savable
from django.contrib.contenttypes.admin import GenericTabularInline

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title',)

class PageInline(admin.TabularInline):
    model = Page
    extra = 1

class ChapterInline(admin.TabularInline):
    model = Chapter
    extra = 1
    inlines = [PageInline]

# Define a generic inline for likes
class LikeInline(GenericTabularInline):
    model = Like
    extra = 1

# Define a generic inline for save
class SaveInline(GenericTabularInline):
    model = Save
    extra = 1

class CommentInline(GenericTabularInline):
    model = Comment
    extra = 1

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [ChapterInline, LikeInline, SaveInline]

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    inlines = [PageInline]


#content on the page
from content.models import Article, Video, Question, Image
class ArticleInline(admin.TabularInline):
    model = Article
    extra = 1

class ImageInline(admin.TabularInline):
    model = Image
    extra = 1

class VideoInline(admin.TabularInline):
    model = Video
    extra = 1

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    inlines = [CommentInline, ArticleInline, ImageInline, VideoInline, QuestionInline]