from django.shortcuts import render, redirect
from django.urls import reverse

def index(request):
    context = {}
    return render(request, 'index.html',context)

