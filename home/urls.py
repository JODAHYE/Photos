"""my_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('home/', include('home.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from home import views
from home.views import PostList, PostDetail, PostListByCategory, PostUpdate, PostCreate, PostDelete, CommentUpdate, \
    MyPostList, MyCommentList, PostListByUser

app_name = 'home'
urlpatterns = [
    path('', PostList.as_view(), name='index'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('category/<str:slug>/', PostListByCategory.as_view(), name='post_list_category'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('<int:pk>/comment_create/', views.comment_create, name='comment_create'),
    path('comment_update/<int:pk>/', CommentUpdate.as_view(), name='comment_update'),
    path('comment_delete/<int:pk>/', views.comment_delete, name='comment_delete'),
    path('my_post/', MyPostList.as_view(), name='my_post_list'),
    path('my_comment/', MyCommentList.as_view(), name='my_comment_list'),
    path('post_like/<int:pk>/', views.post_like, name="post_like"),
    path('user_post/<str:username>/', PostListByUser.as_view(), name='post_list_user'),
    path('about/', views.about, name='about_page'),
]
