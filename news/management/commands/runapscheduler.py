import logging
import datetime

from django.conf import settings
from django.utils import timezone
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from django.core.mail import send_mail, EmailMultiAlternatives

from news.models import Category, Post, UserCategory



logger = logging.getLogger(__name__)


def my_job():
    today = timezone.now()
    time_mail = today - datetime.timedelta(days=30)

    # categories = dict(Category.objects.values('name'))
    emails = Post.objects.filter(created_at__gte=time_mail).values_list('categories__subscribers__email', flat=True)
    # emails = set(emails)
    print('*************')
    print(emails)
    print('*************')
    # subscribers = dict(UserCategory.objects.filter(category=categories).values_list('subscribers'))
    #
    # html_content = render_to_string(
    #     template_name='dailynews.html',
    #     context={
    #         'post':post,
    #         'link':settings.SITE_ID,
    #     }
    # )
    #
    # msg = EmailMultiAlternatives(
    #     subject='Еженедельная сводеа',
    #     body='',
    #     from_email='NewsPeper159@yandex.ru',
    #     id=subscribers,
    #
    # )
    #
    # msg.attach_alternative(html_content, "text/html")
    # msg.send()



def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/1"),
        id = "my_job",
        max_instances = 1,
        replace_existing = True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")