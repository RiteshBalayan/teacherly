from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignupForm, ProfileUpdateForm, VideoCommentForm
from content.models import Video, Article, Image, Question
from course.models import Course
from itertools import chain
from random import shuffle
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from core.forms import CommentForm
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from .models import Profile, VideoComment
from django.contrib.auth.models import User



def user_profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    username = user.username
    user_id = user.id

    courses = Course.objects.filter(teacher=user_id)

    if request.user == user:
        try:
            profile = Profile.objects.get(user_id=user_id)
        except Profile.DoesNotExist:
            # If Profile does not exist, create a new Profile instance
            profile = Profile.objects.create(user_id=request.user)

    return render(request, 'core/user_profile.html', {
        'user': user,
        'user_id': user_id,
        'username': username,
        'courses' : courses,
    
    })

@login_required
def update_profile(request):
    user_id = request.user.id
    profile = Profile.objects.get(user_id=user_id)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile', pk=user_id )  # Redirect to a success page or profile view
    else:
        form = ProfileUpdateForm(instance=profile)

    return render(request, 'core/update_profile.html', {'form': form})


def bitesize(request):
    # Check if the shuffled IDs are already in the session
    if 'shuffled_content_ids' not in request.session:
        # Retrieve the content and shuffle their IDs
        videos = Video.objects.filter(bitesizable=True)
        articles = Article.objects.filter(bitesizable=True)
        images = Image.objects.filter(bitesizable=True)
        video_answers = VideoComment.objects.all()
        #questions = Question.objects.filter(pk=1000)
        
        content_ids = [(obj.__class__.__name__, obj.pk) for obj in chain(videos, articles, images, video_answers)]
        shuffle(content_ids)

        request.session['shuffled_content_ids'] = content_ids
    else:
        # Retrieve the shuffled IDs from the session
        content_ids = request.session['shuffled_content_ids']

    # Fetch the actual objects based on the stored IDs
    def get_object(model_name, pk):
        models = {'Video': Video, 'Article': Article, 'Image': Image, 'VideoComment': VideoComment}
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

    object_id = current_content.object_list[0].id 

    content_type = ContentType.objects.get_for_model(current_content.object_list[0]).model

    content = current_content.object_list[0]


    return render(request, 'core/bitesize.html', {
        'current_content': current_content,
        'comment_form' : comment_form,
        'content_type': content_type,
        'object_id' : object_id,
        'content' : content, 
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

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from .models import Like, Endorse, Save, Comment


def like_object(request, content_type, object_id):
    content_type = ContentType.objects.get(model=content_type)
    model_class = content_type.model_class()
    object_instance = model_class.objects.get(pk=object_id)

    if request.user.is_authenticated:
        try:
            like = Like.objects.get(
                content_type=content_type,
                object_id=object_id,
                user=request.user,
            )
            like.delete()
            liked = False
        except Like.DoesNotExist:
            Like.objects.create(
                content_type=content_type,
                object_id=object_id,
                user=request.user,
            )
            liked = True
        like_count = object_instance.likes.count()  # Get the updated like count
        return JsonResponse({'liked': liked, 'like_count': like_count})
    else:
        return JsonResponse({'error': 'User not authenticated'})

def endorse_object(request, content_type, object_id):
    content_type = ContentType.objects.get(model=content_type)
    model_class = content_type.model_class()
    object_instance = model_class.objects.get(pk=object_id)

    if request.user.is_authenticated:
        try:
            endorse = Endorse.objects.get(
                content_type=content_type,
                object_id=object_id,
                user=request.user,
            )
            endorse.delete()
            endorsed = False
        except Endorse.DoesNotExist:
            Endorse.objects.create(
                content_type=content_type,
                object_id=object_id,
                user=request.user,
            )
            endorsed = True
        endorse_count = object_instance.endorse.count()  # Get the updated like count
        return JsonResponse({'endorsed': endorsed, 'endorse_count': endorse_count})
    else:
        return JsonResponse({'error': 'User not authenticated'})

def save_object(request, content_type, object_id):
    content_type = ContentType.objects.get(model=content_type)

    if request.user.is_authenticated:
        try:
            save = Save.objects.get(
                content_type=content_type,
                object_id=object_id,
                user=request.user,
            )
            save.delete()
            saved = False
        except Save.DoesNotExist:
            Save.objects.create(
                content_type=content_type,
                object_id=object_id,
                user=request.user,
            )
            saved = True
        return JsonResponse({'saved': saved})
    else:
        return JsonResponse({'error': 'User not authenticated'})


from django.core import serializers
import json

def fetch_comments(request, content_type, object_id):
    content_type = ContentType.objects.get(model=content_type)
    comments = Comment.objects.filter(content_type=content_type, object_id=object_id)

    # Prepare a list to hold custom comment data
    comments_data = []

    for comment in comments:
        # Construct a dictionary for each comment with the necessary fields
        comment_data = {
            'id': comment.id,
            'comment': comment.comment,
            'creator_id': comment.creator.id,  # Preserving the original field
            'creator_name': comment.creator.username,  # Adding the username
            # Include any other fields from the Comment model you need
        }

        # Append the custom comment data to the list
        comments_data.append(comment_data)

    # Directly return the JsonResponse without using Django's serializer
    return JsonResponse({'comments': comments_data})


def post_comment(request, content_type, object_id):
    content_type = ContentType.objects.get(model=content_type)
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.creator = request.user
            comment.object_id = object_id
            comment.content_type = content_type
            comment.save()
            return JsonResponse({'status': 'success', 'comment': comment.comment})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    return JsonResponse({'status': 'invalid request'})


def post_video_comment(request, content_type, object_id):
    content_type = ContentType.objects.get(model=content_type)
    if request.method == 'POST':
        form = VideoCommentForm(request.POST, request.FILES)
        if form.is_valid():
            video_comment = form.save(commit=False)
            video_comment.creator = request.user
            video_comment.object_id = object_id
            video_comment.content_type = content_type
            video_comment.save()
            return redirect('forum')  # Redirect to a success page or another relevant view
    else:
        form = VideoCommentForm()

    return render(request, 'core/post_video_comment.html', {'form': form})