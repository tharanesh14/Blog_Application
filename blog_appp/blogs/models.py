from django.db import models

class Authors(models.Model):
    aname = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return self.aname

class Category(models.Model):
    cname = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.cname

class Tag(models.Model):
    tname = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.tname

class BlogPost(models.Model):
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)
    author = models.ForeignKey(Authors, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    notified = models.BooleanField(default=False)

    def __str__(self):
        return self.title

