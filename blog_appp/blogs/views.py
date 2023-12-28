from django.shortcuts import render,  get_object_or_404, redirect
from django.http import request,JsonResponse
from .forms import AuthorsForm,BlogPostForm,CategoryForm, TagForm, CreateUserForm
from .models import Authors,BlogPost
from ajax_datatable import AjaxDatatableView
from django.urls import reverse
from django.template import loader
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user,allowed_user
from django.core.mail import send_mail
from datetime import datetime
from .task import post_mail, edit_mail, notify, delete_mail
# Create your views here.
@login_required(login_url='login')
def home(request):
    notify.delay()
    if request.method == 'POST':
        aform = AuthorsForm(request.POST)
        bform = BlogPostForm(request.POST, request.FILES) 
        catform = CategoryForm(request.POST) 
        tagform = TagForm(request.POST)  
        
        if aform.is_valid():
            aform.save()
            return JsonResponse({"status": "success"})
        # else:
        #     print("is NOT valid:", aform.errors)
        
        if bform.is_valid():
            blog_post=bform.save()
            post_title = blog_post.title 
            user_email = request.user.email 
            post_mail.delay(post_title, user_email)
            print("bfroms saved!")
            return redirect('all')
            # return JsonResponse({"message": "Blog form submitted successfully"})
        
        if catform.is_valid():
            catform.save()
            print("CategoryForm is valid")
            return JsonResponse({"status": "success"})
        else:
            print("CategoryForm is NOT valid:", catform.errors)
        
        if tagform.is_valid():
            tagform.save()
            return JsonResponse({"status": "success"})
        
    else:
        aform = AuthorsForm()
        bform = BlogPostForm()
        catform = CategoryForm()  
        tagform = TagForm()
    
    return render(request, 'home.html', {'aform': aform, 'bform': bform, 'catform': catform, 'tagform': tagform})

@login_required(login_url='login')
def save(request):
    if request.method=='POST':
        data=request.POST.get('hidden')
        if data:
            data=BlogPost.objects.get(pk=data)
            form=BlogPostForm(request.POST,request.FILES,instance=data)
            if form.is_valid():
                data.updated_at = datetime.now()
                blog_post=form.save()
                post_title = blog_post.title 
                user_email = request.user.email 
                edit_mail.delay(post_title, user_email)
                return JsonResponse({'status':'success'})
            return JsonResponse({'status':0})
        else:
            form=BlogPostForm(request.POST,request.FILES)
            if form.is_valid():
                form.save()
                return JsonResponse({'status':'success'})
            return JsonResponse({'status':0})
        
@login_required(login_url='login')
@allowed_user(allowed_roles=['Editor','Publisher'])
def edit(request, pk):
    if request.method == 'GET':
        data = {}  
        datas = get_object_or_404(BlogPost, id=pk)

        data['id'] = datas.id
        data['title'] = datas.title
        data['description'] = datas.description
        data['category'] = datas.category.cname if datas.category else None
        data['published'] = datas.published
        data['author'] = datas.author.aname if datas.author else None
        data['tags'] = [tag.tname for tag in datas.tags.all()]

        return JsonResponse(data)
    else:
        return JsonResponse({'status': 'False'})

def showdata(request, pk):
    try:
        data = BlogPost.objects.get(pk=pk)
        data_data = {
            'title': data.title,
            'description': data.description,
            'category': data.category.cname if data.category else None,
            'created_at': data.created_at,
            'updated_at': data.updated_at,
            'published': data.published,
            'author': data.author.aname if data.author else None,
            'tags': [tag.tname for tag in data.tags.all()],
            'image': data.image.url if data.image else '',
        }
        return JsonResponse({'data_data': data_data})
    except BlogPost.DoesNotExist:
        return JsonResponse({'error': 'data not found'}, status=404)
    

def show(request):
    blog_data = BlogPost.objects.all()
    authors = Authors.objects.all()
    
    return render(request, 'blogs.html', {'blog_data': blog_data, 'authors': authors})

@login_required(login_url='login')
@allowed_user(allowed_roles=['Editor','Publisher'])
def all_blogs(request):
    blog_form =BlogPostForm()
    blog_data = BlogPost.objects.all()
    authors = Authors.objects.all()
    return render(request, 'all.html', {'forms': blog_form,'blog_data': blog_data, 'authors': authors})

@login_required(login_url='login')
@allowed_user(allowed_roles=['Publisher'])
def delete_blog(request, id):
    try:
        blog = BlogPost.objects.get(id=id)
        post_title = blog.title  
        user_email = request.user.email   
        blog.delete()

        delete_mail.delay(post_title, user_email)
        return JsonResponse({"status": "success", "deleted_id": id})
    except BlogPost.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Blog not found"}, status=404)
    
class ajax_table(AjaxDatatableView):
    model = BlogPost
    show_column_filters = False

    column_defs = [
        {'name': 'image', 'visible': True},
        {'name': 'title', 'visible': True, 'orderable': True},
        {'name': 'description', 'visible': True},
        {'name': 'category', 'visible': True, 'searchable':False}, 
        {'name': 'created_at', 'visible': True},
        {'name': 'updated_at', 'visible': True},
        {'name': 'published', 'visible': True},
        {'name': 'author', 'visible': True, 'searchable':False}, 
        {'name': 'tags', 'm2m_foreign_field':'tags__tname' , 'visible': True, 'searchable':False}, 
        {
            "name": "action",
            "visible": True,
            "className": "text-center",
            'searchable':False
        }
    ]

    def customize_row(self, row, obj):
        tags=",".join(tag.tname for tag in obj.tags_list) if obj.tags.exists() else ""
        
        buttons = (
        f'<button type="button" class="btn btn-warning" data-toggle="modal" data-target="#editmodal" onclick="edit(\'{reverse("edit", args=[obj.id])}\')" >Edit</button>'
        + f'<button type="button" class="btn mb-2 btn-outline-link btn-danger " href="javascript:void(0);" onclick="deletes(\'{reverse("delete", args=[obj.id])}\')" >Delete</button>'
        + f'<button type="button" class="btn mb-2 btn-outline-link btn-primary"  data-bs-toggle="modal" data-bs-target="#showmodal" href="javascript:void(0);" onclick="show(\'{reverse("showdata", args=[obj.id])}\')" >Show</button>'
    )
        row["action"] = f'<div class="form-inline justify-content-center">{buttons}</div>'
        return
    
    def get_initial_queryset(self,request=None):
        # if request.user.is_authenticated:
        #     return BlogPost.objects.filter(title=request.POST.get('assigned_user'))
        # else:
        #     return BlogPost.objects.all()
        return BlogPost.objects.all()

@unauthenticated_user
def login(request):
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(request,username=username, password=password)
        if user is not None:
            auth_login(request, user)
            print("Logined success")
            return redirect('show')
        else:
            messages.info(request,"Username or Password is Incorrect!")
            return render(request,"login.html")
    return render(request,"login.html")

def logout(request):
    auth_logout(request)
    return redirect("login")

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                selected_group = form.cleaned_data.get('user_group')
                if selected_group:
                    group, created = Group.objects.get_or_create(name=selected_group)
                    user.groups.add(group)
                messages.success(request, "Account was created successfully")
                return redirect('login')
        else:
            form = CreateUserForm()
    return render(request, "register.html", {'form': form})



#superuser name : t14
#superuser password :t14