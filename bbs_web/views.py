from django.shortcuts import render, redirect
from django.contrib import auth

def index(request):
    context = {}
    return render(request, 'index.html',context)

def login(request):
    username = request.POST.get('username','')
    password = request.POST.get('password','')
    user = auth.authenticate(request, username=username, password=password)
    if user is not None:
        auth.login(request, user)
        return redirect('/')
    else:
        return render(request, 'login_error.html', {'message':'账户或密码错误'})