from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q
from blog.models import Blog

def index(request):
    context = {}
    return render(request, 'index.html',context)

def about(request):
    context ={}
    return render(request, 'about.html',context)

def contact(request):
    context ={}
    return render(request, 'contact.html',context)

def search(request):
    search_words = request.GET.get('wd', '').strip()

    # 分词：按空格 & | ~
    condition = None
    for word in search_words.split(' '):
        if condition is None:
            condition = Q(title__icontains=word)
        else:
            condition = condition | Q(title__icontains=word)
    
    search_blogs = []
    if condition is not None:
        # 筛选：搜索
        search_blogs = Blog.objects.filter(condition)

    # 分页
    paginator = Paginator(search_blogs,10)
    page_num = request.GET.get('page',1)
    page_of_blogs = paginator.get_page(page_num)

    context = {}
    context['search_words'] = search_words
    context['search_blogs_count'] = search_blogs.count()
    context['page_of_blogs'] = page_of_blogs
    return render(request, 'search.html', context)