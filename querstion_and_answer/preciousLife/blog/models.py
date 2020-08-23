from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from taggit.managers import TaggableManager
from hitcount.models import HitCountMixin


from django.contrib.auth import  get_user_model
# Create your models here.

User = get_user_model()

class BlogPost(models.Model, HitCountMixin):
    author                  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogpost')
    blog_title              = models.CharField(unique=True, max_length=264, blank=False, null=False)
    slug                    = models.SlugField(max_length=264)
    blog_description        = models.TextField(max_length=None)
    header_image            = models.ImageField(null=True, blank=True, upload_to='blog_images/')
    tags                    = TaggableManager(blank=True, help_text='Give tags to the blog')
    published_date          = models.DateTimeField()

    def __str__(self):
        return self.blog_title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.blog_title)

        if not self.id:
            self.published_date = timezone.now()
        super().save(*args, **kwargs)
    
    # def get_absolute_url(self):
    #     return reverse("model_detail", kwargs={"pk": self.pk})
    