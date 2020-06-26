from django.shortcuts import render
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect
import hashlib
import os

def about_me(request):
    return render(request, 'articles/about_me.html')

def registration(request):
    return render(request, 'registration.html')

'''hashlib.pbkdf2_hmac(hash_name='sha256',
    password=b'bad_password34',
    salt=b'bad_salt',
    iterations=100000)'''

'''def add_user(request):
    user = User(username = request.POST['username'], password = str(hashlib.pbkdf2_hmac('sha256', request.POST['password'].encode('utf-8'), os.urandom(32), 100000)))
    user.save()
    return HttpResponseRedirect(reverse('list.html'))'''