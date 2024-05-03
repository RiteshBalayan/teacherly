from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import  Comment, Like, Endorse, Save, VideoComment, Profile

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
# Define a generic inline for save
class SaveInline(GenericTabularInline):
    model = Save
    extra = 1

# Define a generic inline for likes
class VideoCommentInline(GenericTabularInline):
    model = VideoComment
    extra = 1

class ReplyInline(GenericTabularInline):
    model = Comment
    fk_name = 'parent_comment'  # Specify the ForeignKey field used for replies

# Register BlogPost and Video models with CommentInline and LikeInlin

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    inlines = [LikeInline, ReplyInline]

admin.site.register(Profile)
admin.site.register(VideoComment)