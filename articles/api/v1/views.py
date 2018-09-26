from django.utils import timezone
from datetime import timedelta
from rest_framework import viewsets, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from articles.models import Article
from .serializers import ArticleSerializer, LikeSerializer


class ArticleViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
    Return a list of all published articles ordered by date.
    """
    serializer_class = ArticleSerializer

    def get_queryset(self):
        gt_72_hours = timezone.now() - timedelta(days=3)
        # filter most top 5 articles w most likes in last 72 hours
        top_five_likes = Article.objects.filter(likes__created__gt=gt_72_hours)\
            .distinct().annotate(likes_counter=Count('likes'))\
            .order_by('-likes_counter')[:5]
        # set the ids to be excludes for next filter
        exclude_ids = [item.id for item in list(top_five_likes)]
        # filter the remaining articles by publish date
        by_date_lt_72hours = Article.objects.filter(publish_date__lte=timezone.now())\
            .annotate(likes_counter=Count('likes'))\
            .order_by('-publish_date')\
            .exclude(id__in=exclude_ids)
        return list(top_five_likes) + list(by_date_lt_72hours)  

class LikeArticle(APIView):

    def post(self, request, pk):
        data = {'article': pk}
        # check for user logged-in
        if request.user.id is not None:
            data['user'] = request.user.id

        serializer = LikeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   
   
