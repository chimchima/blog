from django.contrib import admin
from django.urls import path

from . import views

app_name = 'registration'

urlpatterns = [
    path('', views.index, name = "index"),
    path('add_user', views.RegisterFormView.as_view(), name = "add_user"),
    path('validate_registration_form', views.validate_registration_form, name = "validate_registration_form")
]