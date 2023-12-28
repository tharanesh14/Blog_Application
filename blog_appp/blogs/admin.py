from django.contrib import admin
from .models import Authors,BlogPost, Category, Tag
# Register your models here.
admin.site.register(Authors)
admin.site.register(BlogPost)
admin.site.register(Category)
admin.site.register(Tag)