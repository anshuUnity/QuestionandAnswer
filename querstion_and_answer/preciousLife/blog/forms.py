from django import forms
from blog.models import BlogPost
from django_summernote.widgets import SummernoteWidget

class BlogForm(forms.ModelForm):
    
    class Meta:
        model = BlogPost
        fields = ("blog_title","blog_description", "header_image", "tags",)

        widgets = {
            'blog_description': SummernoteWidget
        }
