# Generated by Django 4.2.3 on 2023-08-17 07:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0005_blogpost_category_tag_delete_blogdata_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='authors',
            old_name='name',
            new_name='aname',
        ),
        migrations.RenameField(
            model_name='category',
            old_name='name',
            new_name='cname',
        ),
        migrations.RenameField(
            model_name='tag',
            old_name='name',
            new_name='tname',
        ),
    ]
