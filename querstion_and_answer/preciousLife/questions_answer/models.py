from django.db import models
from markdownx.models import MarkdownxField
from django.utils.text import slugify
from django.urls import reverse
from taggit.managers import TaggableManager
from django.utils import timezone
from hitcount.models import HitCountMixin

from django.contrib.auth import get_user_model
# QUESTION_ANSWER MODELS 
# Create your models here.

User = get_user_model()

class Question(models.Model, HitCountMixin):
    slug            =models.SlugField(max_length=255)
    title           =models.CharField(max_length=264, blank=False, null=False, unique=True)
    description     =models.TextField(max_length=None)
    published_date  =models.DateTimeField()
    user            =models.ForeignKey(User, on_delete=models.CASCADE, related_name='question')
    tags            =TaggableManager()
    

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        if not self.id:
            self.published_date = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('questions_answer:question_detail', kwargs={'slug':self.slug})


        
