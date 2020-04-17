from django.shortcuts import render, redirect
from django.contrib import auth
from django.urls import reverse

def index(request):
    context = {}
    return render(request, 'index.html',context)

def login(request):
    username = request.POST.get('username','')
    password = request.POST.get('password','')
    user = auth.authenticate(request, username=username, password=password)
    # 获取当前页，获取不到则别名反向解析指向首页
    referer = request.META.get('HTTP_REFERER', reverse('index'))
    if user is not None:
        auth.login(request, user)
        return redirect(referer)
    else:
        return render(request, 'error.html', {'message':'账户或密码错误', 'redirect_to': referer})