# Generated by Django 4.2.3 on 2023-08-31 07:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0007_blogpost_publish_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='publish_date',
        ),
    ]
