from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("home",views.home,name="home"),
    path("",views.show,name="show"),
    path("save",views.save,name="save"),
    path("all",views.all_blogs,name="all"),
    path("delete/<int:id>",views.delete_blog,name="delete"),
    path("edit/<int:pk>",views.edit,name="edit"),
    path("showdata/<int:pk>",views.showdata,name="showdata"),
    path('ajax_table', views.ajax_table.as_view(), name="ajax_table"),
    path("register",views.register,name="register"),
    path("login",views.login,name="login"),
    path("logout",views.logout,name="logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


#superuser name : t14
#superuser password :t14