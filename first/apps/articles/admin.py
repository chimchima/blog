from django.contrib import admin

from .models import Post
admin.site.register(Post)
# Register your models here.

from .models import Article, Comment
admin.site.register(Article)
admin.site.register(Comment)