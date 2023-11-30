from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import VideoForm, ImageForm, ArticleForm, QuestionForm, QuestionOptionForm
from .models import Question
from .forms import QuestionForm, QuestionOptionForm
from core.forms import CommentForm
from django.contrib.contenttypes.models import ContentType


@login_required
def create(request):
    return render(request, 'content/create.html')


@login_required
def ask_question(request):
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)

        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.user = request.user
            question.bitesizable = True
            question.save()

            return redirect('forum')
    else:
        question_form = QuestionForm()

    return render(request, 'content/ask_question.html', {
        'question_form': question_form, 
        })


def question(request, pk):
    question = get_object_or_404(Question, pk=pk)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.creator = request.user
            comment.content_type = ContentType.objects.get_for_model(question)  # Assuming Page is the model you want to associate comments with
            comment.object_id = question.id  # Get the ID of the current page
            comment.save()
            return redirect('question', pk=question.id)

    else:
        comment_form = CommentForm()

    return render(request, 'content/question.html', {
        'question': question,
        'comment_form' : comment_form,
    })

@login_required
def create_video(request):
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
    return render(request, 'content/video_form.html', {'form': form})

@login_required
def create_image(request):
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
    return render(request, 'content/image_form.html', {'form': form})

@login_required
def create_article(request):
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
    return render(request, 'content/article_form.html', {'form': form})
