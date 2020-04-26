在shell 下编写文章

~~~python
>>> from article.models import ArticlePost
>>> from django.contrib.auth.models import User
>>> article = ArticlePost()
>>> article.title = "shell 下的第一篇文章"
>>> article.body = "我在shell下写文章"
>>> user = User.objects.all()[0]
>>> article.save()
~~~

shell 下查看内容

~~~python
>>> from article.models import ArticlePost
>>> dir()
['ArticlePost', 'Paginator', '__builtins__', 'objects', 'p']

>>> from django.contrib.auth.models import User
>>> User.objects.all()
<QuerySet [<User: william>, <User: rainbow>, <User: Austinwilliam>, <User: tony>]>
~~~

shell for循环生成

~~~python
>>> for i in range(1,50):
...     article = ArticlePost()
...     article.title = "shell下的第 %s" %i
...     article.body = "我用for循环生成的文章：%s" %i
...     article.author = user
...     article.save()
~~~



#### 分页器实现分页

~~~python
from django.core.paginator import Paginator
// 分页的页表，每几篇文章分一页
paginator = Paginator(object_list,each_page_count)
// 具体页面
page1 = paginator.page(1)
~~~



~~~python
>>> from django.core.paginator import Paginator
>>> from article.models import ArticlePost
>>> articles = ArticlePost.objects.all()
>>> articles.count()
52
>>> paginator = Paginator(articles,10)
>>> dir(paginator)
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_check_object_list_is_ordered', '_get_page', 'allow_empty_first_page', 'count', 'get_page', 'num_pages', 'object_list', 'orphans', 'page', 'page_range', 'per_page', 'validate_number']
>>> paginator.count
52
>>> paginator.num_pages
6
>>> paginator.page_range
range(1, 7)
>>> page1 = paginator.page(1)
>>> page1
<Page 1 of 6>
>>> dir(page1)
['__abstractmethods__', '__class__', '__contains__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__', '__setattr__', '__sizeof__', '__slots__', '__str__', '__subclasshook__', '__weakref__', '_abc_impl', 'count', 'end_index', 'has_next', 'has_other_pages', 'has_previous', 'index', 'next_page_number', 'number', 'object_list', 'paginator', 'previous_page_number', 'start_index']
>>> help(page1.has_previous)
Help on method has_previous in module django.core.paginator:

has_previous() method of django.core.paginator.Page instance

>>> page1.object_list
<QuerySet [<ArticlePost: shell下的第 49>, <ArticlePost: shell下的第 48>, <ArticlePost: shell下的第 47>, <ArticlePost: shell下的第 46>, <ArticlePost: shell下的第 45>, <ArticlePost: shell下的第 44>, <ArticlePost: shell下的第 43>, <ArticlePost: shell下的第 42>, <ArticlePost: shell下的第 41>, <ArticlePost: shell下的第 40>]>

>>> page2 = paginator.page(2)
>>> page2.has_next()
True
>>> page2.has_previous()
True
>>> page3 = paginator.page(1)
>>> page3.has_previous()
False
>>> page3.next_page_number()
2
>>>
~~~



#### 用户搜索

**search**参数，存放需要搜索的文本。若search不为空，则检索特定文章对象

icontains 不区分大小写而 contains区分大小写

如果用户没有搜索，search = ‘’ 否在，search=None



#### filter筛选条件

​	a. 大于：__gt(greater than)

​	b. 大于等于：__gte

​	c. 小于：__lt(less than)

​	d. 小于等于：__lte

​	e. 包含：__contains(不加i忽略大小写)

​	f. 开头是： __startswith

​	g. 结尾是： __endswith

​	h. 其中之一： __in

​	i. 范围： __range	

​	j. 等于：直接筛选