from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Count
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.contenttypes.models import ContentType

from .models import Blog, BlogType
from .forms import BlogForm
from read_statistics.utils import read_statistics_once_read
from comment.models import Comment
from comment.forms import CommentForm

# from user.forms import loginForm



def get_blog_list_common_data(request,blogs_all_list):
     # 分页器
    paginator = Paginator(blogs_all_list,settings.EACH_PAGE_BLOGS_NUMBER) # 每7篇进行分页
    page_num = request.GET.get('page',1) # 获取url的页面参数（GET请求）
    page_of_blogs = paginator.get_page(page_num)
    currentr_page_num = page_of_blogs.number # 获取当前页
    # 获取当前页前后各两页的页码范围
    page_range = list(range(max(currentr_page_num-2,1), currentr_page_num)) + \
                list(range(currentr_page_num,min(currentr_page_num+2,paginator.num_pages)+1))
    # 加上省略页码标记
    if page_range[0] -1 >= 2:
        page_range.insert(0,"...")
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append("...")
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0,1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    # 获取博客分类的对应博客数量
    # BlogType.objects.annotate(blog_count=Count('blog'))
    '''
    blog_types = BlogType.objects.all()
    blog_types_list = []
    for blog_type in blog_types:
        blog_type.blog_count = Blog.objects.filter(blog_type=blog_type).count()
        blog_types_list.append(blog_type)
    '''

    # 获取日期归档对应的博客数量
    blog_dates = Blog.objects.dates('created_time','month',order='DESC')
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year,
                                        created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count
    
    context = {}
    # 博客列表
    context['blogs'] = page_of_blogs.object_list
    # 当前页
    context['page_of_blogs'] = page_of_blogs
    # 页码范围
    context['page_range'] = page_range
    # 全部分类
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
    # 时间归档
    context['blog_dates'] = blog_dates_dict
    return context
    
def blog_list(request):
    blogs_all_list = Blog.objects.all()
    context = get_blog_list_common_data(request, blogs_all_list)
    return render(request, 'blog/blog_list.html',context)

def blogs_with_type(request,blog_type_pk):
    blog_type = get_object_or_404(BlogType,pk=blog_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    context = get_blog_list_common_data(request, blogs_all_list)
    context['blog_type'] = blog_type
    return render(request, 'blog/blogs_with_type.html',context)

def blogs_with_date(request, year, month):
    blogs_all_list = Blog.objects.filter(created_time__year=year,created_time__month=month)
    context = get_blog_list_common_data(request, blogs_all_list)
    context['blogs_with_date'] = '%s年%s月' % (year,month)
    return render(request, 'blog/blogs_with_date.html',context)

def blog_detail(request, blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)
    read_cookie_key = read_statistics_once_read(request,blog)
    blog_content_type = ContentType.objects.get_for_model(blog)
    comments = Comment.objects.filter(content_type=blog_content_type, object_id=blog.pk)

    context = {}
    # 筛选当前博客大于创建时间博客的最后一条
    context['next_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    # 筛选当前博客大于创建时间博客的第一条
    context['previous_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    context['blog'] = blog
    context['comments'] = comments
    context['comment_form'] = CommentForm(initial={'content_type':blog_content_type.model, 'object_id':blog_pk})
    response = render(request, 'blog/blog_detail.html',context)
    response.set_cookie(read_cookie_key,'true') # 阅读cookie标记
    return response

def blog_create(request):
    # 判断用户是否提交数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        blog_post_form = BlogForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if blog_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_blog = blog_post_form.save(commit=False)
            # 指定数据库中作者id
            new_blog.author = User.objects.get(id=request.user.id)

            if request.POST['blog_type'] != 'none':
                new_blog.blog_type = BlogType.objects.get(id=request.POST['blog_type'])
            else:
                return HttpResponse("请填写分类！")

            # 将新文章保存到数据库中
            new_blog.save()
            # 完成后返回到文章列表
            return redirect("blog_list")
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 如果用户请求获取数据
    else:
        article_post_form = BlogForm()
        context = {}
        blog_types = BlogType.objects.all()
        context['article_post_from'] = article_post_form
        context['blog_types'] = blog_types
        return render(request, 'blog/blog_create.html', context)


def blog_delete(request, id):
    # 根据 id 获取需要删除的文章
    blog = Blog.objects.get(id=id)
    # 过滤非作者的用户
    if request.user != blog.author:
        return HttpResponse("您没有删除这篇文章的权限.")
    # 调用.delete()方法删除文章
    blog.delete()
    # 完成删除后返回文章列表
    return redirect("blog_list")

def blog_update(request,id):
    # 获取需要修改的具体文章对象
    blog = Blog.objects.get(id=id)
    # 判断用户是否为 POST 提交表单数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        blog_post_form = BlogForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if blog_post_form.is_valid():
            # 保存新写入的 title、body 数据并保存
            blog.title = request.POST['title']
            blog.content = request.POST['content']
            blog.save()
            # 完成后返回到修改后的文章中。需传入文章的 id 值
            return redirect("blog_list")
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")

    # 如果用户 GET 请求获取数据
    else:
        # 创建表单类实例
        blog_post_form = BlogForm()

        context = {}
        context['blog'] = blog
        context['blog_post_from'] = blog_post_form
        return render(request, 'blog/blog_update.html', context)
