from django.utils import timezone

from django.conf import settings
from django.db import models
from django_extensions.db.fields import AutoSlugField
from django_extensions.db.models import TimeStampedModel


def get_timestamp_path(root, filename):
    """
    Return a path with the format <root>/<timestamp>-<filename>
    """
    return '{}/{}-{}'.format(
        root,
        int(timezone.now().timestamp()),
        filename
    )


def author_avatar_path(instance, filename):
    return get_timestamp_path('author-avatar', filename)


def article_image_path(instance, filename):
    return get_timestamp_path('article-image', filename)


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name')

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Author(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=author_avatar_path, null=True, blank=True)
    slug = AutoSlugField(populate_from=['user__first_name', 'user__last_name'])

    def __str__(self):
        return self.name

    @property
    def name(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)


class Article(TimeStampedModel):
    title = models.CharField(max_length=250)
    hero = models.ImageField(upload_to=article_image_path, null=True, blank=True)
    content = models.TextField()

    slug = AutoSlugField(populate_from=['publish_date', 'title'])
    publish_date = models.DateField()

    author = models.ForeignKey(Author, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title


class Like(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Article, related_name='likes', null=False, on_delete=models.CASCADE)   
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_likes', null=True, on_delete=models.CASCADE)
    slug = AutoSlugField(populate_from=['created', 'article'])

    class Meta:
        verbose_name_plural = 'Gostei'

    def __str__(self):
        return '{}-{}@{}'.format(self.article, self.created, self.user)
