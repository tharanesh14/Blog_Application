from django import forms
from .models import Category, Tag, BlogPost, Authors
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django import forms

class AuthorsForm(forms.ModelForm):
    class Meta:
        model = Authors
        fields = ['aname']
        widgets = {
            'aname': forms.TextInput(attrs={'class': 'form-control', 'id': 'authorname'}),
        }
        labels = {
            'aname': 'Author Name', 
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['cname']
        widgets = {
            'cname': forms.TextInput(attrs={'class': 'form-control', 'id': 'categoryname'}),
        }
        labels = {
            'cname': 'Category Name', 
        }

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['tname']
        widgets = {
            'tname': forms.TextInput(attrs={'class': 'form-control', 'id': 'tagname'}),
        }
        labels = {
            'tname': 'Tag Name', 
        }

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        exclude = ['created_at', 'updated_at'] 
        fields = ['title', 'description', 'category', 'image', 'published', 'author', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'id': 'title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'id': 'description'}),
            'category': forms.Select(attrs={'class': 'form-control', 'id': 'category'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'id': 'image'}),
            'published': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'published'}),
            'author': forms.Select(attrs={'class': 'form-control', 'id': 'author'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control', 'multiple': 'multiple', 'id': 'tags'}),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['category'].queryset = Category.objects.all()
            self.fields['author'].queryset = Authors.objects.all()
            self.fields['tags'].queryset = Tag.objects.all()
            
            self.fields['author'].widget = forms.Select(attrs={'class': 'form-control', 'id': 'author'})
            self.fields['author'].widget.choices = [(author.id, author.aname) for author in Authors.objects.all()]
            
            self.fields['author'].label_from_instance = lambda obj: f'{obj.aname}'
            



class CreateUserForm(UserCreationForm):
    user_group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label="Select a user group",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control'