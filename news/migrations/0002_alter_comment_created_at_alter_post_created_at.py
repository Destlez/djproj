# Generated by Django 4.2.16 on 2024-09-17 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_at',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='post',
            name='created_at',
            field=models.TextField(),
        ),
    ]
