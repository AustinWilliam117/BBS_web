from django.urls import path
from . import views

urlpatterns = [
    # http://localhost:8000/read_statistics
    path('',views.read_statistics,name='read_statistics'),
]