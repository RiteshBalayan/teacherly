from rest_framework import serializers
from content.models import Video, Article, Image

class VideoSerializer(serializers.ModelSerializer):
    content_type = serializers.CharField(default='video')

    class Meta:
        model = Video
        fields = '__all__'

class ArticleSerializer(serializers.ModelSerializer):
    content_type = serializers.CharField(default='article')

    class Meta:
        model = Article
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
    content_type = serializers.CharField(default='image')

    class Meta:
        model = Image
        fields = '__all__'

