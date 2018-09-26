from django.urls import path, include
from rest_framework import routers

from .views import ArticleViewSet, LikeArticle


article_router = routers.SimpleRouter()
article_router.register('articles', ArticleViewSet, base_name='articles')

urlpatterns = [
    path('', include(article_router.urls)),
    path("articles/like/<int:pk>", LikeArticle.as_view(), name="like-article"),
]

