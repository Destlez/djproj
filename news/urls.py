from .views import *
from django.urls import path

from django.views.decorators.cache import cache_page

app_name='news_name_app'

urlpatterns = [
    path('', cache_page(60)(PostList.as_view()), name='post_list'),
    path('<int:pk>', cache_page(300)(OnePost.as_view()), name='onepost'),
    path('news/create/', CreateForm.as_view(), name='crpost'),
    path('news/<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('article/create/', CreateForm.as_view(), name='crpost'),
    path('article/<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('article/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('search/', Search.as_view()),
    path('category/', CategoryPost.as_view(), name='category'),
    path('catlist/<int:pk>', CategoryList.as_view(), name='catlist'),
    path('catlist/<int:pk>/subs/', add_subscribers, name='subs'),
    path('home/', ewn.as_view()),


]
