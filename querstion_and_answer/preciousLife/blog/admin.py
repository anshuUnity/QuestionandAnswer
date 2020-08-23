from django.contrib import admin
from blog.models import BlogPost
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.

class BlogAdmin(SummernoteModelAdmin):
    summernote_fields = ('blog_description',)

admin.site.register(BlogPost, BlogAdmin)