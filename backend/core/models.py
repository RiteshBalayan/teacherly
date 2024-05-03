from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey ,GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError



class Profile(models.Model):

    user_id = models.OneToOneField(User, related_name='Profile', on_delete=models.CASCADE)
    description = models.CharField(max_length = 500, blank=True)
    profile_pic = models.ImageField(upload_to='profil_pic', blank=True)

    def __str__(self):
        return f"Profile of {self.user_id.username}"


class Like(models.Model):
    
    # Generic Foreign Key to associate comments with different models
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # Model specific fields
    user = models.ForeignKey(User, on_delete=models.CASCADE )

    class Meta:
        unique_together = (("content_type", "object_id", "user"),)

    def save(self, *args, **kwargs):
        existing_like = Like.objects.filter(
            content_type=self.content_type,
            object_id=self.object_id,
            user=self.user
        )
        if existing_like.exists():
            raise ValidationError("You have already liked this content.")
        else:
            super(Like, self).save(*args, **kwargs)

class Likable(models.Model):
    likes = GenericRelation(Like)

    class Meta:
        abstract = True

class Endorse(models.Model):
    
    # Generic Foreign Key to associate comments with different models
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # Model specific fields
    user = models.ForeignKey(User, on_delete=models.CASCADE )

    class Meta:
        unique_together = (("content_type", "object_id", "user"),)

    def save(self, *args, **kwargs):
        existing_endorse = Endorse.objects.filter(
            content_type=self.content_type,
            object_id=self.object_id,
            user=self.user
        )
        if existing_endorse.exists():
            raise ValidationError("You have already endorse this content.")
        else:
            super(Endorse, self).save(*args, **kwargs)

class Endorsable(models.Model):
    endorse = GenericRelation(Endorse)

    class Meta:
        abstract = True

class Save(models.Model):
    
    # Generic Foreign Key to associate comments with different models
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # Model specific fields
    user = models.ForeignKey(User, on_delete=models.CASCADE )

    class Meta:
        unique_together = (("content_type", "object_id", "user"),)

    def save(self, *args, **kwargs):
        existing_save = Save.objects.filter(
            content_type=self.content_type,
            object_id=self.object_id,
            user=self.user
        )
        if existing_save.exists():
            raise ValidationError("You have already save this content.")
        else:
            super(Save, self).save(*args, **kwargs)

class Savable(models.Model):
    saves = GenericRelation(Save)

    class Meta:
        abstract = True

class Comment(Likable):

    # Generic Foreign Key to associate comments with different models
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # Self-referencing field for replies to comments
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    # Model specific fields
    creator = models.ForeignKey(User, on_delete=models.CASCADE )
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)


class Commentable(models.Model):
    comments = GenericRelation(Comment)

    class Meta:
        abstract = True

class VideoComment(Likable, Savable):

    # Generic Foreign Key to associate comments with different models
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # Self-referencing field for replies to comments
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    # Model specific fields
    creator = models.ForeignKey(User, on_delete=models.CASCADE )
    comment = models.FileField(upload_to='Video_comment/')
    created = models.DateTimeField(auto_now_add=True)

class VideoCommentable(models.Model):
    VideoComment = GenericRelation(Comment)

    class Meta:
        abstract = True


