from django import forms

from .models import Blog

# 写文章的表单类
class BlogForm(forms.ModelForm):
    class Meta:
        # 指明数据模型来源
        model = Blog
        # 定义表单包含的字段
        fields = ('title', 'content')

