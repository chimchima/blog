from django.http import Http404, HttpResponseForbidden, HttpResponse, HttpResponseRedirect, JsonResponse

from django.utils import timezone

from django.urls import reverse

from django.db import models

from .models import Article, Comment, Answer

from django.shortcuts import render

import json

from django.core import serializers

import os

import hashlib

from django.views.decorators.csrf import csrf_exempt

import pymorphy2
morph = pymorphy2.MorphAnalyzer()

'''class ArticleEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Article):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)'''

def index(request):
	latest_articles_list = Article.objects.order_by('-pub_date')
	com = {article.article_title: morph.parse('комментарий')[0].make_agree_with_number(article.comments).word for article in latest_articles_list}
	return render(request, 'articles/list.html', {'latest_articles_list': latest_articles_list, 'com': com})

def test(request):
	name = 'anton'
	name = name.encode('utf-8')
	data = str(hashlib.pbkdf2_hmac('sha256', name, os.urandom(32), 100000))
	return HttpResponse(data)

def test2(request):
	arr = ['sqqcc', 'cijppio']
	data = json.dumps(arr)
	data = json.loads(data)
	return HttpResponse(data[1])
	#return HttpResponse('I love coding')

def detail(request, article_id):
	try:
		a = Article.objects.get( id = article_id )
		a.views += 1
		a.save()
	except:
		raise Http404("Article not found")
	latest_comments_list = a.comment_set.order_by('-id')[:10]
	answers_list = Answer.objects.all()
	return render(request, 'articles/detail.html', {'article': a, 'latest_comments_list': latest_comments_list, 'json_comments_list': serializers.serialize('json', latest_comments_list), 'answers': answers_list})

def leave_comment(request, article_id):
	try:
		a = Article.objects.get( id = article_id )
		a.comments += 1
		a.save()
	except:
		raise Http404("Article not found")
	#comment = a.comment_set.create(author_name = request.user.username, comment_text = request.POST['text'], date_pub = timezone.now())
	comment = a.comment_set.create(author_name = request.user.username, comment_text = request.GET.get('text'), date_pub = timezone.now())
	comment.save()
	#return HttpResponseRedirect(reverse('articles:detail', args=(a.id,)))
	return JsonResponse({'response': 'ok'})

def get_json_comments(request, article_id):
	a = Article.objects.get(id = article_id)
	comments = a.comment_set.order_by('-id')
	return HttpResponse(serializers.serialize('json', comments))

def create(request):
	if request.user.is_authenticated:
		return render(request, 'articles/create.html')
	else:
		return HttpResponseForbidden('log in to create articles')
		#return HttpResponse('log in to create articles')

def new(request):
	#render(request, 'articles/list.html')
	art = Article(article_title = request.POST['title'], article_txt = request.POST.get('text'), pub_date = timezone.now(), author_name = request.POST.get('username'))
	art.save()
	#return HttpResponseRedirect(reverse('articles:list'))
	render(request, 'articles/list.html')
	return HttpResponseRedirect(reverse('articles:detail', args=(art.id,)))

def about_me(request):
	return render(request, 'articles/about_me.html')

def addlike(request, article_id):
	#render(request, 'articles:detail')
	#render(request, 'articles/' + str(request.POST['art_id']) + '/')
	article = Article.objects.get(id = article_id)
	likers = article.likers.split(sep = ' ')
	if request.user.is_authenticated:
		if request.user.username not in likers:
			article.likes += 1
			likers.append(request.user.username)
			likers_str = ''
			for elem in likers:
				likers_str = likers_str + elem + ' '
			article.likers = likers_str
			article.save()
		else:
			article.likes -= 1
			likers = likers[:likers.index(request.user.username)] + likers[likers.index(request.user.username) + 1:]
			likers_str = ''
			for elem in likers:
				likers_str = likers_str + elem + ' '
			article.likers = likers_str
			article.save()
	#url = 'articles/' + request.POST['art_id']
	#return render(request, 'articles/list.html')
	#return index(request)
	#return render(request, "articles/{{request.POST['art_id']}}")
	#latest_comments_list = article.comment_set.order_by('-id')[:10]
	#return render(request, 'articles/detail.html', {'article': article, 'latest_comments_list': latest_comments_list})
	return HttpResponseRedirect(reverse('articles:detail', args=(article.id,)))

def get_all_articles(request):
	all_articles = Article.objects.all()
	'''for article in all_articles:
		article = json.dumps(article, cls=ArticleEncoder)
	#data = json.dump(all_articles)
	return HttpResponse(all_articles)'''
	'''for article in all_articles:
		article = {'title': article.article_title, 'text': article.article_txt, 'author': article.author_name, 'pub_date': article.pub_date, 'comments': article.comments, 'likes': article.likes}
	#return HttpResponse(all_articles, content_type='application/json')'''
	#data = json.dumps(all_articles)
	data = serializers.serialize('json', all_articles)
	return HttpResponse(data, content_type='application/json')

def delete(request, article_id):
	article = Article.objects.get(id = article_id)
	article.delete()
	return HttpResponseRedirect('../../../articles/')

def delete_comment(request, comment_id):
	#comment = Comment.objects.get(id = request.POST['comment_id'])
	comment = Comment.objects.get(id = comment_id)
	comment.delete()
	article = Article.objects.get(id = comment.article.id)
	article.comments -= 1
	article.save()
	return HttpResponseRedirect(reverse('articles:detail', args=(article.id,)))

def like_comment(request, comment_id):
	comment = Comment.objects.get(id = comment_id)
	likers = comment.likers.split(sep = ' ')
	if request.user.is_authenticated:
		if request.user.username not in likers:
			comment.likes += 1
			likers.append(request.user.username)
			likers_str = ''
			for elem in likers:
				likers_str = likers_str + elem + ' '
			comment.likers = likers_str
			comment.save()
		else:
			comment.likes -= 1
			likers = likers[:likers.index(request.user.username)] + likers[likers.index(request.user.username) + 1:]
			likers_str = ''
			for elem in likers:
				likers_str = likers_str + elem + ' '
			comment.likers = likers_str
			comment.save()
	return HttpResponseRedirect(reverse('articles:detail', args=(comment.article.id,)))

def add_answer(request, comment_id):
	comment = Comment.objects.get(id = comment_id)
	answer = Answer(text = request.POST['answer_text'], comment = comment, author_name = request.user.username, pub_date = timezone.now())
	answer.save()
	comment.answers += 1
	comment.save()
	article = Article.objects.get(id = comment.article.id)
	article.comments += 1
	article.save()
	return HttpResponseRedirect(reverse('articles:detail', args = (article.id,)))

def like_answer(request, answer_id):
	answer = Answer.objects.get(id = answer_id)
	likers = answer.likers.split(sep = ' ')
	if request.user.is_authenticated:
		if request.user.username not in likers:
			answer.likes += 1
			likers.append(request.user.username)
			likers_str = ''
			for elem in likers:
				likers_str = likers_str + elem + ' '
			answer.likers = likers_str
			answer.save()
		else:
			answer.likes -= 1
			likers = likers[:likers.index(request.user.username)] + likers[likers.index(request.user.username) + 1:]
			likers_str = ''
			for elem in likers:
				likers_str = likers_str + elem + ' '
			answer.likers = likers_str
			answer.save()
	return HttpResponseRedirect(reverse('articles:detail', args = (Comment.objects.get(id = answer.comment.id).article.id,)))

def delete_answer(request, answer_id):
	answer = Answer.objects.get(id = answer_id)
	answer.delete()
	comment = Comment.objects.get(id = answer.comment_id)
	article = Article.objects.get(id = comment.article.id)
	comment.answers -= 1
	comment.save()
	article.comments -= 1
	article.save()
	return HttpResponseRedirect(reverse('articles:detail', args = (Comment.objects.get(id = answer.comment_id).article.id,)))

def add_ajax(request): 
	print('Hello world')
	response = {'first-text': 'Lorem Ipsum is simply dummy text', 'second-text': 'to make a type specimen book. It has '}
	return JsonResponse(response)
	#return HttpResponse('Hello world')'

'''
    if request.is_ajax():
        response = {'first-text': 'Lorem Ipsum is simply dummy text', 'second-text': 'to make a type specimen book. It has '}
        return JsonResponse(response)
    else:
        raise Http404'''