from django.contrib import admin
from blog.models import BlogPost, CommentBlogPost, TaggedBlog
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.

class BlogAdmin(SummernoteModelAdmin):
    summernote_fields = ('blog_description',)
    list_display = ('blog_title','pk')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('published_date','comment_content')

admin.site.register(BlogPost, BlogAdmin)
admin.site.register(CommentBlogPost, CommentAdmin)
admin.site.register(TaggedBlog)