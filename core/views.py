from django.shortcuts import render, redirect
from .forms import SignupForm
from content.models import Video, Article, Image, Question
from course.models import Course
from itertools import chain
from random import shuffle
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from core.forms import CommentForm
from django.contrib.contenttypes.models import ContentType


def bitesize(request):
    # Check if the shuffled IDs are already in the session
    if 'shuffled_content_ids' not in request.session:
        # Retrieve the content and shuffle their IDs
        videos = Video.objects.filter(bitesizable=True)
        articles = Article.objects.filter(bitesizable=True)
        images = Image.objects.filter(bitesizable=True)
        questions = Question.objects.filter(pk=1000)
        
        content_ids = [(obj.__class__.__name__, obj.pk) for obj in chain(videos, articles, images, questions)]
        shuffle(content_ids)

        request.session['shuffled_content_ids'] = content_ids
    else:
        # Retrieve the shuffled IDs from the session
        content_ids = request.session['shuffled_content_ids']

    # Fetch the actual objects based on the stored IDs
    def get_object(model_name, pk):
        models = {'Video': Video, 'Article': Article, 'Image': Image, 'Question': Question}
        return models[model_name].objects.get(pk=pk)

    content = [get_object(model_name, pk) for model_name, pk in content_ids]

    paginator = Paginator(content, 1)
    page = request.GET.get('page', 1)

    try:
        current_content = paginator.page(page)
    except PageNotAnInteger:
        current_content = paginator.page(1)
    except EmptyPage:
        current_content = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.creator = request.user
            comment.content_type = ContentType.objects.get_for_model(current_content.object_list[0])  # Assuming Page is the model you want to associate comments with
            comment.object_id = current_content.object_list[0].id  # Get the ID of the current page
            comment.save()
            # Build the URL with the 'content' query parameter to return to the same page
            redirect_url = request.path_info + f'?page={current_content.number}'
            return redirect(redirect_url)

    else:
        comment_form = CommentForm()

    return render(request, 'core/bitesize.html', {
        'current_content': current_content,
        'comment_form' : comment_form,
        })

def courses_view(request):
    courses = Course.objects.all()

    return render(request, 'core/courses.html', {
        'courses' : courses
    })

def forum(request):
    questions = Question.objects.filter(bitesizable=True)
    return render(request, 'core/forum.html', {
        'questions': questions
    })


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/login/')
    else:
        form = SignupForm()

    return render(request, 'core/signup.html', {
        'form': form
    })

