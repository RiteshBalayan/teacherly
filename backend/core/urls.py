from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from .forms import LoginForm

from .DRFviews import TikTokFeed

urlpatterns = [
    path('', views.bitesize, name='bitesize'),
    path('profile/<int:pk>/', views.user_profile, name='user_profile'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('like/<str:content_type>/<int:object_id>/', views.like_object, name='like_object'),
    path('endorse/<str:content_type>/<int:object_id>/', views.endorse_object, name='endorse_object'),
    path('save/<str:content_type>/<int:object_id>/', views.save_object, name='save_object'),
    path('fetchcomments/<str:content_type>/<int:object_id>/', views.fetch_comments, name='fetch_comments'),
    path('post_comment/<str:content_type>/<int:object_id>/', views.post_comment, name='post_comment'),
    path('post_video_comment/<str:content_type>/<int:object_id>/', views.post_video_comment, name='post_video_comment'),
    path('cources/', views.courses_view, name='courses'), 
    path('forum/', views.forum, name='forum'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),


    path('tiktok-feed/', TikTokFeed.as_view(), name='tiktok_feed'),
]