from django.db import models
from django.contrib.auth.models import User
from core.models import Commentable, Likable, Savable, Profile

class Topic(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Course(Likable, Savable):
    title = models.CharField(max_length=100)
    thumbnail = models.ImageField(upload_to='course_thumbnails/')  
    description = models.TextField()
    topics = models.ManyToManyField(Topic, blank=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='taught_courses')
    students = models.ManyToManyField(User, related_name='enrolled_courses', blank=True)

    def __str__(self):
        return self.title

class Chapter(models.Model):
    title = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='chapters')
    serial_number = models.PositiveIntegerField(default=0, editable=True)

    def __str__(self):
        return f"{self.course.title} | {self.title}"

    def save(self, *args, **kwargs):
        if not self.pk:  # If it's a new chapter being created
            last_chapter = Chapter.objects.filter(course=self.course).order_by('-serial_number').first()
            if last_chapter:
                self.serial_number = last_chapter.serial_number + 1
            else:
                self.serial_number = 1
        super().save(*args, **kwargs)


class Page(Commentable):
    CONTENT_TYPE_CHOICES = [
        ('video', 'Video'),
        ('article', 'Article'),
        ('question', 'Question'),
        ('image', 'image'),
    ]

    title = models.CharField(max_length=100)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='page')
    serial_number = models.PositiveIntegerField(default=0, editable=True)

    def __str__(self):
        return f"{self.chapter.course.title} | {self.chapter.title} | {self.title}"

    def save(self, *args, **kwargs):
        if not self.pk:  # If it's a new chapter being created
            last_page = Page.objects.filter(chapter=self.chapter).order_by('-serial_number').first()
            if last_page:
                self.serial_number = last_page.serial_number + 1
            else:
                self.serial_number = 1
        super().save(*args, **kwargs)

class StudentProgress(models.Model):
    student = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='StudentProgress')
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='page_StudentProgress')
    clicked = models.BooleanField(default=False)

    class Meta:
        unique_together = ['student', 'page']

    def __str__(self):
        return f"{self.student.user_id} - {self.page.chapter}|{self.page.title} - Clicked: {self.clicked}"
