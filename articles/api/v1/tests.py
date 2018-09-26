from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.urls import reverse
from django.utils import timezone

from articles.models import Article, Author, Category, Like


User = get_user_model()


def create_author(alias=''):
    user = User.objects.create_user(
        email='test{}@test.com'.format(alias),
        password='secret',
        first_name='Test {}'.format(alias),
        last_name='Tester {}'.format(alias)
    )
    return Author.objects.create(user=user, avatar=ContentFile('picture', name='avatar.jpeg'))


def create_category(alias=''):
    return Category.objects.create(name='category{}'.format(alias))


def create_article(author, category, publish_date, alias=''):
    return Article.objects.create(
        title='Title {}'.format(alias),
        content='Content {}'.format(alias),
        hero=ContentFile('picture', name='hero.jpeg'),
        author=author,
        category=category,
        publish_date=publish_date,
    )

def create_like(article,created=timezone.now()):
    user = User.objects.create_user(
        email='test-like@test.com',
        password='secret',
        first_name='Test',
        last_name='Tester like'
    )
    return Like.objects.create(
        article=article,
        user=user,
        created=created
    )


@pytest.mark.django_db(transaction=False)
def test_articles_schema(client):
    author = create_author()
    category = create_category()

    today = timezone.now().date() - timedelta(days=1)
    article = create_article(author, category, today)

    like = create_like(article)

    url = reverse('articles-list')
    response = client.get(url)

    article = response.json()[0]
    assert list(article.keys()) == [
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
    ]
    assert list(article['author'].keys()) == ['slug', 'name', 'avatar']
    assert list(article['category'].keys()) == ['slug', 'name']
    assert list(article['likes'][0].keys()) == [ 'slug','user','created','article']


@pytest.mark.django_db(transaction=False)
def test_articles_list(client):

    author = create_author('author test 1')
    category = create_category('category test 1')
    user = User.objects.create_user(
        email='test-like@test.com',
        password='secret',
        first_name='Test',
        last_name='Tester like'
    )

    for i in range(0,5):       
        today = timezone.now().date() - timedelta(days=1)        
        article = create_article(author, category, today, 'Top likes {}'.format(str(i+1)))
        for j in range(0,(i+1)):
            like = create_like(article,user)

    for i in range(0,5):       
        today = timezone.now().date() - timedelta(days=(i+1))        
        article = create_article(author, category, today, 'Top dates {}'.format(str(i+1)))
        like = create_like(article,user)


    url = reverse('articles-list')
    response = client.get(url)

    articles = response.json()
    assert len(list(articles[0]['likes'])) == 5
    assert len(list(articles[1]['likes'])) == 4
    assert len(list(articles[2]['likes'])) == 3
    assert len(list(articles[3]['likes'])) == 2
    assert len(list(articles[4]['likes'])) == 1
    assert articles[5]['publish_date'] == str(timezone.now().date() - timedelta(days=1))
    assert articles[6]['publish_date'] == str(timezone.now().date() - timedelta(days=2))
    assert articles[7]['publish_date'] == str(timezone.now().date() - timedelta(days=3))
    assert articles[8]['publish_date'] == str(timezone.now().date() - timedelta(days=4))
    assert articles[9]['publish_date'] == str(timezone.now().date() - timedelta(days=5))

