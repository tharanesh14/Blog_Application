from celery import shared_task
from django.core.mail import send_mail
from django.http import request
from .models import BlogPost
from django.contrib.auth.models import Group
from django.utils import timezone
from datetime import timedelta

from .models import BlogPost

@shared_task(bind=True)
def post_mail(self, post_title, user_email):
    send_mail(
        f'New Blog Post: {post_title}',
        f'A new blog post with title "{post_title}" has been published.\nUse this url to view blogs : http://127.0.0.1:8000/',
        'your_email@example.com',
        [user_email], 
        fail_silently=False
    )
    return "Blog Post Notification Sent"

@shared_task(bind=True)
def edit_mail(self, post_title, user_email):
    send_mail(
        f'Updated Blog Post: {post_title}',
        f'The blog post with title "{post_title}" has been updated.\nUse this url to view blogs : http://127.0.0.1:8000/',
        'your_email@example.com',
        [user_email], 
        fail_silently=False
    )
    return "Blog Post Update Notification Sent"

@shared_task(bind=True)
def delete_mail(self, post_title, user_email):
    send_mail(
        f'Deleted Blog Post: {post_title}',
        f'The blog post with title "{post_title}" has been deleted.',
        'your_email@example.com',
        [user_email],
        fail_silently=False
    )
    return "Blog Post Deletion Notification Sent"

@shared_task
def notify():
    roles = ['Author', 'Editor', 'Publisher']
    
    recipients = []
    for role in roles:
        group = Group.objects.get(name=role)
        recipients.extend(group.user_set.filter(is_active=True).values_list('email', flat=True))
    
    if recipients:
        current_time = timezone.now()
        past_time = current_time - timedelta(minutes=5) # Calculate 5 minutes ago (I will only work if the task i created within 5 minutes before)
                                                        # If task created within 5 minutes then it will send mail to all the users like to "Check out new Blog !"
        new_blogs = BlogPost.objects.filter(published=True, notified=False, created_at__gte=past_time)
        
        for blog in new_blogs:
            subject = f'New Blog Published: {blog.title}'
            message = f'A new blog titled "{blog.title}" has been published. Check it Out!\nUse this url to view blogs : http://127.0.0.1:8000/'
            send_mail(subject, message, 'your_email@example.com', recipients)
            blog.notified = True
            blog.save()


