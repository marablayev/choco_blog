
from rest_framework import serializers

from account.serializers import AuthorSerializer
from .models import Post, Category, Comment


class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(required=False)

    class Meta:
        model = Comment
        fields = ('id', 'author', 'publish_date', 'text')


class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Post
        fields = ('id', 'title', 'slug', 'image', 'text', 'rating', \
                  'publish_date', 'category', 'author')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title', 'slug')
