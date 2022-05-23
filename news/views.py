from email.mime import image
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def welcome(request):
    return HttpResponse('welcome to The Moringa Tribune')
