from django.urls import path
from .views import *
from django.urls import path

app_name='news_name_app'

urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>', OnePost.as_view(), name='onepost'),
    path('news/create/', CreateForm.as_view(), name='crpost'),
    path('news/<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('article/create/', CreateForm.as_view(), name='crpost'),
    path('article/<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('article/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('search/', Search.as_view()),
    path('category/', CategoryPost.as_view(), name='category'),
    path('catlist/<int:pk>', CategoryList.as_view(), name='catlist'),
    path('catlist/<int:pk>/subs/', subs_category, name='subs'),


]
