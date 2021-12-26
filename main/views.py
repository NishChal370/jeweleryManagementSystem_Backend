from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(response):
    return HttpResponse("Hello from API")