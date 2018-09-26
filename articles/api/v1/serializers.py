from rest_framework import serializers

from articles.models import Article, Author, Category, Like


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = (
            'slug',
            'name',
            'avatar',
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'slug',
            'name',
        )


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = (
            'slug',
            'user',
            'created',
            'article'
        )


class ArticleSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    author = AuthorSerializer()
    category = CategorySerializer()
    likes = LikeSerializer(many=True, read_only=True, required=False)
    likes_counter = serializers.IntegerField()

    class Meta:
        model = Article
        fields = (
            'id',
            'author',
            'category',
            'title',
            'content',
            'hero',
            'slug',
            'publish_date',
            'likes',
            'likes_counter'
        )
