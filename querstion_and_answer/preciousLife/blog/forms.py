from django import forms
from blog.models import BlogPost, CommentBlogPost
from django_summernote.widgets import SummernoteWidget

class BlogForm(forms.ModelForm):
    
    class Meta:
        model = BlogPost
        fields = ("blog_title","blog_description", "header_image", "tags",)

        widgets = {
            'blog_description': SummernoteWidget
        }

class CommentBlogForm(forms.ModelForm):

    class Meta:
        model = CommentBlogPost
        fields= ("comment_content",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comment_content'].label = ""
        self.fields['comment_content'].widget.attrs.update({'class' : 'comment_content'})

        # giving place holders to fields
        self.fields['comment_content'].widget.attrs.update({'placeholder':'Write your thoughts about the blog'})