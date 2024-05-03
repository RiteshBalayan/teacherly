from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create, name='create'),
    path('ask_question/', views.ask_question, name = 'ask_question'),
    path('question/<int:pk>', views.question, name = 'question'),
    path('create/video/', views.create_video, name='create_video'),
    path('create/image/', views.create_image, name='create_image'),
    path('create/article/', views.create_article, name='create_article'),
]
