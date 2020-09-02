from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone
from taggit.managers import TaggableManager
from hitcount.models import HitCountMixin,HitCount
from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError

from django.contrib.auth import  get_user_model
# Create your models here.

User = get_user_model()

def validate_file_size(value):
    filesize= value.size
    
    if filesize > 5242880:
        raise ValidationError("The Image size should be less than 5mb")
    else:
        return value

class BlogPost(models.Model, HitCountMixin):
    author                  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogpost')
    blog_title              = models.CharField(unique=True, max_length=264, blank=False, null=False)
    slug                    = models.SlugField(max_length=264)
    blog_description        = models.TextField(max_length=None)
    header_image            = models.ImageField(null=True, blank=True, upload_to='blog_images/',validators = [validate_file_size])
    tags                    = TaggableManager(blank=True, help_text='Give tags to the blog')
    published_date          = models.DateTimeField()
    likes                   = models.ManyToManyField(User, related_name='blog_likes', blank=True)
    favorite                = models.ManyToManyField(User, related_name='favorite_blog', blank=True)
    hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation')  

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return self.blog_title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.blog_title)

        if not self.id:
            self.published_date = timezone.now()
        super().save(*args, **kwargs)

    def total_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse('blog:blog_detail', kwargs={'slug':self.slug})
    
    # def get_absolute_url(self):
    #     return reverse("model_detail", kwargs={"pk": self.pk})

class CommentBlogPost(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_content = models.TextField(blank=False, null=False)
    blogpost        = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    published_date  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment_content

    class Meta:
        ordering = ['-published_date']
