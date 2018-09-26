from datetime import timedelta
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
    return Like.objects.create(
        article=article,       
        created=created
    )



def run():

    author = create_author('author test 1')
    category = create_category('category test 1')

    for i in range(0,5):       
        today = timezone.now().date() - timedelta(days=1)        
        article = create_article(author, category, today, 'Top likes {}'.format(str(i+1)))
        for j in range(0,(i+1)):
            like = create_like(article)

    for i in range(0,5):       
        today = timezone.now().date() - timedelta(days=(i+1))        
        article = create_article(author, category, today, 'Top dates {}'.format(str(i+1)))
        like = create_like(article)
    
    print('--end of script--')

    


# execute script remotely
# heroku run python manage.py shell
# exec(open('dumpdb.py').read())
run()
