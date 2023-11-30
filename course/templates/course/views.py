from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, Chapter, Page
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import CourseForm, ChapterForm, PageForm
from django.contrib.auth.decorators import login_required
from content.models import Article, Image, Video, Question
# Create your views here.

def course_view(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'course/course.html', {
        'course':course
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

    return render(request, 'course/chapter.html', {
        'current_page': current_page,
        'course':course,
        'chapter':chapter,
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
def create_video_course(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.user = request.user
            video.bitesizable = True
            video.save()
            return redirect('/')
    else:
        form = VideoForm()
    return render(request, 'content/video_form_content.html', {'form': form})

@login_required
def create_image_course(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = request.user
            image.bitesizable = True
            image.save()
            return redirect('/')
    else:
        form = ImageForm()
    return render(request, 'content/image_form_content.html', {'form': form})

@login_required
def create_article_course(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.bitesizable = True
            article.save()
            return redirect('/')
    else:
        form = ArticleForm()
    return render(request, 'content/article_form_content.html', {'form': form})



