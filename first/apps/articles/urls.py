from django.contrib import admin
from django.urls import path

from . import views

app_name = 'articles'
urlpatterns = [
	#path('admin/', admin.site.urls),
	path('', views.index, name = 'index'),
	path('test/', views.test, name = 'test'),
	path('test2/', views.test2, name = 'new_test'),
	path('<int:article_id>/', views.detail, name = 'detail'),
	path('<int:article_id>/leave_comment/', views.leave_comment, name = 'leave_comment'),
	path('create/', views.create, name = 'create'),
	path('new/', views.new, name = 'new'),
	path('about_me/', views.about_me, name = 'about_me'),
	path('<int:article_id>/addlike/', views.addlike, name = "addlike"),
	path('get_all_articles/', views.get_all_articles, name = "get_all_articles"),
	path('<int:article_id>/delete/', views.delete, name = "delete"),
	path('<int:comment_id>/delete_comment/', views.delete_comment, name = "delete_comment"),
	path('<int:comment_id>/like_comment/', views.like_comment, name = "like_comment"),
	path('<int:comment_id>/add_answer/', views.add_answer, name = "add_answer"),
	path('<int:answer_id>/like_answer/', views.like_answer, name = "like_answer"),
	path('<int:answer_id>/delete_answer/', views.delete_answer, name = "delete_answer"),
	#url(r'^ajax/$', views.add_ajax)
	path('add_ajax/', views.add_ajax, name = "add_ajax"),
	path('<int:article_id>/get_json_comments/', views.get_json_comments, name = "get_json_comments")
]