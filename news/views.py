from datetime import datetime, timezone, timedelta
from lib2to3.fixes.fix_input import context

from django.db.transaction import commit
from django.http import HttpResponseRedirect, HttpResponse
from unicodedata import category

from .forms import *
from django.urls import  reverse_lazy
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views import View
from .tasks import every_week_news

from django.core.paginator import Paginator






from .filters import NewsFilter
from .models import *

class PostList(ListView):
    model = Post
    ordering = 'created_at'
    template_name = 'news.html'
    context_object_name = 'news_cont'
    paginate_by = 10





class OnePost(DetailView):
    model = Post
    template_name = 'firstnews.html'
    context_object_name = 'news_one'


    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        post=self.object
        category=post.categories.all()
        if post.categories:
            context['category_name']=category
        else:
            context['category_name']=None
        return context


def post_mp(request):
    form=Newsforms()
    if request.method == 'POST':
        form=Newsforms(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/create/')
    return render(request,'form_post.html', {'form': form})

class CreateForm(PermissionRequiredMixin, CreateView):
    model = Post
    form_class = Newsforms
    template_name = 'form_post.html'
    permission_required = ('news.created_at',)


    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/news/news/create/':
            post.post_type = 'news'
        else:
            post.post_type = 'Article'
        post.author = self.request.user.author
        post.save()
        return super().form_valid(form)




class PostUpdate(PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = Newsforms
    template_name = 'form_post.html'
    permission_required = ('news.created_at',)

class PostDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_del.html'
    success_url = reverse_lazy('post_list')
    permission_required = ('news.created_at',)

class Search(ListView):
    model = Post
    template_name = 'search.html'
    paginate_by = 10
    context_object_name = 'news_cont'
    ordering = '-created_at'


    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        if self.request.GET:
            context['has_results'] = self.filterset.qs.exists()
        else:
            context['has_results'] = False
        return context


def userlist(request):
    author=Author.objects.all()
    return render(request,'search.html',{'author': author})

class CategoryPost(ListView):
    model = Category
    ordering = 'name'
    template_name = 'category.html'
    context_object_name = 'categorypost'

class CategoryList(DetailView):
    model = Category
    template_name = 'catlist.html'
    context_object_name = 'catlist'

    def get_queryset(self):
        return Category.objects.all()

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        category=self.get_object()
        context['news_list']=Post.objects.filter(categories=category)
        return context

# @login_required
# def subs_category(request, pk):
#     category = Category.objects.get(id=pk)
#     created = Category.objects.get_or_create(user=request.user, subscribers=category)
#
#     if created:
#         return redirect('/')
#     else:
#         return redirect("/sign/login/")
#     return redirect('news_name_app:subs')
@login_required
def add_subscribers(request, pk):
    user = request.user
    category = get_object_or_404(Category, id=pk)

    if user in category.subscribers.all():
        message = 'Вы уже подписаны на эту категорию: '
    else:
        category.subscribers.add(user)
        message = 'Вы подписались на рассылку новостей: '

    return render(request, 'subscr.html', {'category': category, 'message': message})

class ewn(View):
    def get(self, request):
        every_week_news.delay()
        return HttpResponse('text/html!')



def listing(request):
    contact_list = PostList.objects.all()
    paginator = Paginator(contact_list, 10) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'news.html', {'page_obj': page_obj})


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'style': '{',
    'formatters': {
        'main_format': {
            'format': '%(asctime)s %(levelname)s %(message)s',
            'datefmt': "%d.%m.%Y %H-%M-%S"
        },
        'main_warning': {
            'format': '%(asctime)s %(levelname)s %(pathname)s %(message)s',
            'datefmt': "%d.%m.%Y %H-%M-%S"
        },
        'main_error': {
            'format': '%(asctime)s %(levelname)s %(pathname)s %(message)s %(exc_info)s',
            'datefmt': "%d.%m.%Y %H-%M-%S"
        },
        'general_log': {
            'format': '%(asctime)s %(levelname)s %(module)s %(message)s',
            'datefmt': "%d.%m.%Y %H-%M-%S"
        },
        'errors_log': {
            'format': '%(asctime)s %(levelname)s %(message)s %(pathname)s %(exc_info)s',
            'datefmt': "%d.%m.%Y %H-%M-%S"
        },
        'security_log': {
            'format': '%(asctime)s %(levelname)s %(module)s %(message)s',
            'datefmt': "%d.%m.%Y %H-%M-%S"
        },
        'email': {
            'format': '%(asctime)s %(levelname)s %(message)s %(pathname)s',
            'datefmt': "%d.%m.%Y %H-%M-%S"
        }
    },
'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler', #класс обработчика, который выводит информацию в консоль
            'formatter': 'main_format'
        },
        'console_warning': {
            'level': 'WARNING',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'main_warning'
        },
        'console_error': {
            'level': 'ERROR',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'main_error'
        },
        'general': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'logging.FileHandler',  #класс обработчика для записи в файл
            'filename': 'logs/general.log', #путь и имя файла
            'formatter': 'general_log'
        },
        'errors': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'logs/errors.log',
            'formatter': 'errors_log'
        },
        'security': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/security.log',
            'formatter': 'security_log'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'email'
        }
    },
'loggers': {
        'django': {
            'handlers': ['console', 'console_error', 'console_warning', 'general'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['errors', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.server': {
            'handlers': ['errors', 'mail_admins'],
            'propagate': True,
        },
        'django.template': {
            'handlers': ['errors'],
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['errors'],
            'propagate': True,
        },
        'django.security': {
            'handlers': ['security'],
            'propagate': True,
        },
    }
}