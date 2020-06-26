from django.http import Http404, HttpResponse, HttpResponseRedirect

from django.views.generic.edit import FormView

from django.views.generic.base import View

from django.views.generic import TemplateView

from django.contrib.auth.forms import UserCreationForm

from django.urls import reverse

from django.db import models

from django.shortcuts import render

from django.contrib.auth.models import User

from passlib.hash import pbkdf2_sha256

import hashlib

import os

from django.contrib.auth.forms import UserCreationForm

from passlib.hash import bcrypt_sha256

#from .models import User

def index(request):
    return render(request, 'registration.html', {'form': UserCreationForm})

class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = 'articles/'
    template_name = 'registration.html'

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)
    
    def form_invalid(self, form):
        return super(RegisterFormView, self).form_invalid(form)

'''def sign_up(request):
    user = User(username = request.POST['username'], password = request.POST['password'])
    user.save()
    return HttpResponse('Welcome ' + user.username + '!')

def log_in(request):
    return render(request, 'log_in.html')

def authorisation(request):
    username = request.POST['username']
    password = request.POST['password']
    try :
        user = User.objects.get(username = username)
        if user.password == password :
            return HttpResponse('Welcome ' + username + '!')
        else :
            wrong = True
            return HttpResponseRedirect(reverse('registration:log_in'))
    except :
        notfound = True
        return HttpResponseRedirect(reverse('registration:log_in'))
        #return render(request, 'log_in.html', notfound)'''

def validate_registration_form(request):
    form = UserCreationForm(request.GET)
    #return HttpResponse(form.is_valid())
    if form.is_valid:
        pass
    else:
        return super(RegisterFormView, self).form_invalid(form)

def add_user(request):
    f = UserCreationForm(request.POST)
    if f.is_valid():
        f.save()
    return HttpResponseRedirect(reverse('articles:index'))