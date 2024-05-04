from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from itertools import chain
from random import shuffle
from content.models import Video, Image, Article
from .serializers import VideoSerializer, ImageSerializer, ArticleSerializer
from .forms import CommentForm
from django.contrib.contenttypes.models import ContentType

class CustomPagination(PageNumberPagination):
    page_size = 1  # Keep is strickly one, otherwise some gliches may appear
    page_size_query_param = 'page_size'
    max_page_size = 100

class TikTokFeed(APIView):
    pagination_class = CustomPagination

    def get_queryset(self):
        videos = Video.objects.filter(bitesizable=True)
        images = Image.objects.filter(bitesizable=True)
        article = Article.objects.filter(bitesizable=True)
        combined_data = list(videos) + list(images) + list(article)
        shuffle(combined_data)  # Change it with personalised recomendation sysyem later on

        return combined_data

    def get(self, request):
        queryset = self.get_queryset()

        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(queryset, request)
        
        data = []
        for item in result_page:
            if isinstance(item, Video):
                serializer = VideoSerializer(item)
            elif isinstance(item, Image):
                serializer = ImageSerializer(item)
            elif isinstance(item, Article):
                serializer = ArticleSerializer(item)
            data.append(serializer.data)


        return paginator.get_paginated_response(data)
