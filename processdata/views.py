from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template import loader
# Create your views here.


def index(request):
    return render(request, template_name='index.html')
