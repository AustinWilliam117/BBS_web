# BBS_web设计



## 本地运行

可以使用 Virtualenv在本地运行项目。

> **注意：**
>
> 本项目的虚拟环境为Linux系统，Linux可通过`source ll_env/bin/activate`运行虚拟环境。
>
> Windows系统下删除ll_env 文件夹，请使用python3.5及以上版本运行搭建虚拟环境`python -m venv ll_env ` 
>
> 虚拟环境的安装`pip install --user virtualenv` 
>
> Windows下虚拟环境的激活`ll_env\Scripts\activate`

克隆到本地

~~~bash
$ git clone https://github.com/AustinWilliam117/AustinWilliam117.git
~~~

#### Virtualenv

1. 在创建和激活虚拟环境后，安装项目依赖包

   ~~~bash
   $ pip install -r requirements.txt
   ~~~
   

2. 运行开发服务器

   ~~~bash
   $ python manage.py runserver
   ~~~

   

3. 浏览器访问：http://127.0.0.1:8000，可进入到博客首页

