# Generated by Django 4.2.3 on 2023-08-31 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0006_rename_name_authors_aname_rename_name_category_cname_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='publish_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
