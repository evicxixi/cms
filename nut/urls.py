"""nut URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from cms import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index, name='index'),
    re_path('^$', views.cms),
    path('login/', views.login, name='login'),
    path('code/', views.code, name='code'),
    path('logout/', views.logout, name='logout'),
    path('upload/', views.upload, name='upload'),
    path('comment/', views.comment, name='comment'),
    path('article_up_down/', views.article_up_down, name='article_up_down'),

    path('dashboard/', views.dashboard, name='dashboard'),
    re_path('dashboard/article/(?P<article>\d+)',
            views.dashboard, name='dashboard'),

    re_path('cms/$', views.cms, name='cms'),
    re_path('(?P<username>\w+)/$', views.cms, name='cms'),
    re_path('(?P<username>\w+)/(?P<key>cate|tag|p)/(?P<value>.*)/',
            views.cms, name='cms'),
    re_path('^article/(\d+)', views.article, name='article'),
]
