import datetime
# from NewsPeper.NewsPeper import settings
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Category, Post
from django.utils import timezone



@shared_task
def every_week_news(pk):
    post = Post.objects.get(pk=pk)
    categories = post.category.all()
    subscribers_list = []

    for c in categories:
        subscribers = c.subscribers.all()
        subscribers_list += [s for s in subscribers]

    for s in subscribers_list:
        sub_name = s.username
        sub_email = [s.email]
        html_content = render_to_string(
            'dailynews.html',
            {
                'text': post.preview(),
                'link': f'http://127.0.0.1:8000/news/{pk}',
                'sub_name': sub_name
            }
        )
        msg = EmailMultiAlternatives(
            subject=post.title,
            body='',
            from_email='NewsPeper159@yandex.ru',
            to=sub_email
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()