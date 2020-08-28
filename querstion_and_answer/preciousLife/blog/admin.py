from django.contrib import admin
from blog.models import BlogPost, CommentBlogPost
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.

class BlogAdmin(SummernoteModelAdmin):
    summernote_fields = ('blog_description',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('published_date','comment_content')

admin.site.register(BlogPost, BlogAdmin)
admin.site.register(CommentBlogPost, CommentAdmin)