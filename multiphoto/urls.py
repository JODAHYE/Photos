"""photo_site URL Configuration

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from multiphoto import views
from multiphoto.views import MultiList, MultiDetail, MultiDelete, CommentUpdate, MyMultiList, MyMultiCommentList, \
    MultiListByUser

app_name = 'multiphoto'
urlpatterns = [
    path('', MultiList.as_view(), name='index'),
    path('<int:pk>/', MultiDetail.as_view(), name='multi_detail'),
    path('<int:pk>/update/', views.multi_update, name='multi_update'),
    path('create/', views.multi_create, name='multi_create'),
    path('about/', views.multi_about, name='multi_about'),
    path('<int:pk>/delete/', MultiDelete.as_view(), name='multi_delete'),
    path('<int:pk>/comment_create/', views.comment_create, name='comment_create'),
    path('comment_update/<int:pk>/', CommentUpdate.as_view(), name='comment_update'),
    path('comment_delete/<int:pk>/', views.comment_delete, name='comment_delete'),
    path('my_post/', MyMultiList.as_view(), name='my_multi_list'),
    path('my_comment/', MyMultiCommentList.as_view(), name='my_multi_comment_list'),
#    path('multi_like/<int:pk>/', views.multi_like, name="multi_like"),
    path('user_post/<str:username>/', MultiListByUser.as_view(), name='multi_list_user'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

