from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, Chapter, Page
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import CourseForm, ChapterForm, PageForm, VideoFormCourse, ImageFormCourse, ArticleFormCourse
from django.contrib.auth.decorators import login_required
from content.models import Article, Image, Video, Question
from core.forms import CommentForm
from django.contrib.contenttypes.models import ContentType

# Create your views here.

def course_view(request, pk):
    course = get_object_or_404(Course, pk=pk)
    first_chapter = Chapter.objects.filter(pk=course.id).first()
    return render(request, 'course/course.html', {
        'course':course,
        'first_chapter': first_chapter,
    })


def Chapter_view(request, pk, chapter_pk):
    course = get_object_or_404(Course, pk=pk)
    chapter = get_object_or_404(Chapter, pk=chapter_pk)
    pages = chapter.page.all()

    paginator = Paginator(pages, 1)
    page = request.GET.get('page', 1)

    try:
        current_page = paginator.page(page)
    except PageNotAnInteger:
        current_page = paginator.page(1)
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.creator = request.user
            comment.content_type = ContentType.objects.get_for_model(Page)  # Assuming Page is the model you want to associate comments with
            comment.object_id = current_page.object_list[0].id  # Get the ID of the current page
            comment.save()
            # Build the URL with the 'page' query parameter to return to the same page
            redirect_url = request.path_info + f'?page={current_page.number}'
            return redirect(redirect_url)

    else:
        comment_form = CommentForm()

    return render(request, 'course/chapter.html', {
        'current_page': current_page,
        'course':course,
        'chapter':chapter,
        'comment_form': comment_form,
    })

@login_required
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user
            course.save()
            return redirect('create_chapter', pk=course.id)
    else:
        form = CourseForm()

    return render(request, 'course/create_course.html',{
        'form' : form,
    })
    
@login_required
def create_chapter(request, pk):
    course = get_object_or_404(Course, pk=pk)
    chapters = Chapter.objects.filter(course=course)
    if request.method == 'POST':
        form = ChapterForm(request.POST)
        if form.is_valid():
            chapter = form.save(commit=False)
            chapter.course = course
            chapter.save()
            return redirect('create_chapter', pk=course.id)
    else:
        form = ChapterForm()

    return render(request, 'course/create_chapter.html',{
        'form' : form,
        'course': course,
        'chapters':chapters,
    })

@login_required
def create_page(request, pk, chapter_pk):
    course = get_object_or_404(Course, pk=pk)
    chapter = get_object_or_404(Chapter, pk=chapter_pk)
    pages = Page.objects.filter(chapter=chapter)
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save(commit=False)
            page.chapter = chapter
            page.save()
            return redirect('create_page', pk=course.id, chapter_pk=chapter.id)
    else:
        form = PageForm()

    return render(request, 'course/create_page.html',{
        'form' : form,
        'course': course,
        'chapter':chapter,
        'pages':pages,
    })

@login_required
def page(request, pk, chapter_pk, page_pk):
    course = get_object_or_404(Course, pk=pk)
    chapter = get_object_or_404(Chapter, pk=chapter_pk)
    page = get_object_or_404(Page, pk=page_pk)

    articles = Article.objects.filter(course=page)
    images = Image.objects.filter(course=page)
    videos = Video.objects.filter(course=page)
    questions = Video.objects.filter(course=page)


    return render(request, 'course/page.html', {
        'course' : course,
        'chapter' : chapter,
        'page' : page,
        'articles' : articles,
        'images': images,
        'videos': videos,
        'questions' : questions,
    })


@login_required
def add_page(request, pk, chapter_pk, page_pk):
    course = get_object_or_404(Course, pk=pk)
    chapter = get_object_or_404(Chapter, pk=chapter_pk)
    page = get_object_or_404(Page, pk=page_pk)

    return render(request, 'course/add_page.html', {
        'course' : course,
        'chapter' : chapter,
        'page' : page,
    })

@login_required
def create_video_course(request, pk, chapter_pk, page_pk):
    course = get_object_or_404(Course, pk=pk)
    chapter = get_object_or_404(Chapter, pk=chapter_pk)
    page = get_object_or_404(Page, pk=page_pk)
    if request.method == 'POST':
        form = VideoFormCourse(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.user = request.user
            video.course = page
            video.save()
            return redirect('page', pk=course.id, chapter_pk=chapter.id, page_pk=page.id)
    else:
        form = VideoFormCourse()
    return render(request, 'course/video_form_content.html', {
        'form': form,
        'course' : course,
        'chapter' : chapter,
        'page' : page,
        })

@login_required
def create_image_course(request, pk, chapter_pk, page_pk):
    course = get_object_or_404(Course, pk=pk)
    chapter = get_object_or_404(Chapter, pk=chapter_pk)
    page = get_object_or_404(Page, pk=page_pk)
    if request.method == 'POST':
        form = ImageFormCourse(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = request.user
            image.course = page
            image.save()
            return redirect('page', pk=course.id, chapter_pk=chapter.id, page_pk=page.id)
    else:
        form = ImageFormCourse()
    return render(request, 'course/image_form_content.html', {
        'form': form,
        'course' : course,
        'chapter' : chapter,
        'page' : page,
        })

@login_required
def create_article_course(request, pk, chapter_pk, page_pk):
    course = get_object_or_404(Course, pk=pk)
    chapter = get_object_or_404(Chapter, pk=chapter_pk)
    page = get_object_or_404(Page, pk=page_pk)
    if request.method == 'POST':
        form = ArticleFormCourse(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.course = page
            article.save()
            return redirect('page', pk=course.id, chapter_pk=chapter.id, page_pk=page.id)
    else:
        form = ArticleFormCourse()
    return render(request, 'course/article_form_content.html', {
        'form': form,
        'course' : course,
        'chapter' : chapter,
        'page' : page,
        })



