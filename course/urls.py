from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/', views.course_view, name='course'),
    path('<int:pk>/<int:chapter_pk>/', views.Chapter_view, name='chapter'),
    path('create_course/', views.create_course, name='create_course'),
    path('edit/<int:pk>/', views.create_chapter, name='create_chapter'),
    path('edit/<int:pk>/<int:chapter_pk>/', views.create_page, name='create_page'),
    path('edit/<int:pk>/<int:chapter_pk>/<int:page_pk>/', views.page, name='page'),
    path('edit/<int:pk>/<int:chapter_pk>/<int:page_pk>/add/', views.add_page, name='add_page'),
    path('edit/<int:pk>/<int:chapter_pk>/<int:page_pk>/video/', views.create_video_course, name='create_video_course'),
    path('edit/<int:pk>/<int:chapter_pk>/<int:page_pk>/image/', views.create_image_course, name='create_image_course'),
    path('edit/<int:pk>/<int:chapter_pk>/<int:page_pk>/article/', views.create_article_course, name='create_article_course'),

]