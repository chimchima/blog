import datetime
from django.db import models
from django.utils import timezone
from django.contrib.postgres import fields 
''' import ArrayField'''
# Create your models here.
class Article(models.Model):
    article_title = models.CharField('article name', max_length = 100, null = True)
    article_txt = models.TextField('article text', max_length = 2000)
    pub_date = models.DateTimeField('publication date')
    comments = models.IntegerField('artcle_comments', default = 0)
    likes = models.IntegerField('likes', default = 0)
    author_name = models.CharField('article name', max_length = 100, null = True)
    views = models.BigIntegerField('views', default = 0)
    likers = models.TextField('likers', default = '')
    #likers = fields.ArrayField('likers', default = [])
    objects = models.Manager()

    '''def __init__(self):
        self.comments = len(Comment.objects.get(article_name = self.article_title))'''

    def __str__(self):
        return self.article_title

    def was_published_recently(self):
        '''now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now'''
        return self.pub_date >= (timezone.now() - datetime.timedelta(days=3)) and self.pub_date <= timezone.now()

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete = models.CASCADE)
    author_name = models.CharField('author name', max_length = 50)
    comment_text = models.CharField('comment text', max_length = 200)
    date_pub = models.DateTimeField('comment publication date')
    answers = models.IntegerField('comment answers', default = 0)
    likes = models.IntegerField('comment likes', default = 0)
    likers = models.TextField('comment likers', default = '')
    objects = models.Manager()

    '''def __init__(self):
        self.article_name = Article.objects.get( id = self.article ).article_title'''

    '''def __str__(self):
        return self.author_name'''

    def __str__(self):
        return "Comment" + str(self.id)

class Answer(models.Model):
    text = models.TextField('answer text', max_length=200)
    author_name = models.CharField('author name', max_length = 50)
    pub_date = models.DateTimeField('answer publication date')
    comment = models.ForeignKey(Comment, on_delete = models.CASCADE)
    likes = models.IntegerField('answer likes', default = 0)
    likers = models.TextField('answer likers', default = '')
    objects = models.Manager()

    def __str__(self):
        return "Answer" + str(self.id)

class Post(models.Model):
    title = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, unique=True)
    body = models.TextField(max_length=150, db_index=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return '{}'.format(self.title)


