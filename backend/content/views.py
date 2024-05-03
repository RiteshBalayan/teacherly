from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import VideoForm, ImageForm, ArticleForm, QuestionForm, QuestionOptionForm
from .models import Question
from .forms import QuestionForm, QuestionOptionForm
from core.forms import CommentForm
from django.contrib.contenttypes.models import ContentType
from core.models import Like, Endorse, Save, Comment, VideoComment
from django.db.models import Count


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

    #data to pass for generic realtions, see java script in base.html
    content_type = ContentType.objects.get_for_model(question)
    object_id = question.id
    # Annotate each VideoComment with the count of related likes and order them
    top_video_comments = VideoComment.objects.filter(
        content_type=content_type, 
        object_id=object_id
    )
    # Get the top liked video comment if it exists
    top_video_comment = top_video_comments.first() if top_video_comments.exists() else None

    return render(request, 'content/question.html', {
        'question': question,
        'content_type': content_type.model,
        'object_id': object_id,
        'top_video_comment':top_video_comment,
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
