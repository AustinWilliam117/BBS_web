
from django.contrib import admin
from django.urls import include,path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('ckeditor', include('ckeditor_uploader.urls')),
    path('blog/', include('blog.urls')),
    path('comment/', include('comment.urls')),
    path('read_statistics/', include('read_statistics.urls')),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)