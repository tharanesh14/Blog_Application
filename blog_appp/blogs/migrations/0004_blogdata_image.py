# Generated by Django 4.2.4 on 2023-08-16 19:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blogs", "0003_alter_authors_name_alter_blogdata_title"),
    ]

    operations = [
        migrations.AddField(
            model_name="blogdata",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="blog_images/"),
        ),
    ]