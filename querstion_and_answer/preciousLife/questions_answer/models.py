from django.db import models
from markdownx.models import MarkdownxField
from django.utils.text import slugify
from django.urls import reverse
from taggit.managers import TaggableManager
from django.utils import timezone
from hitcount.models import HitCountMixin


from django.contrib.auth import get_user_model
from accounts.models import UserProfileInfo
# QUESTION_ANSWER MODELS 
# Create your models here.

User = get_user_model()

class Question(models.Model, HitCountMixin):
    slug              =models.SlugField(max_length=255)
    title             =models.CharField(max_length=264, blank=False, null=False, unique=True)
    description       =models.TextField(max_length=None, blank=False, null=False)
    published_date    =models.DateTimeField()
    user              =models.ForeignKey(User, on_delete=models.CASCADE, related_name='question')
    tags              =TaggableManager(blank=True, help_text='Give the tags to the question')
    likes             =models.ManyToManyField(User, related_name='likes') 
 
    

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

    def total_likes(self):
        return self.likes.count()

class Images(models.Model):
    question            = models.ForeignKey(Question, on_delete=models.CASCADE)
    image             = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return self.question.title + ' images'


class Answer(models.Model):
    questions                = models.ForeignKey(Question, on_delete=models.CASCADE, blank=True)
    answer_description      = models.TextField(blank=False, null=False, verbose_name='answer_desc')
    published_at            = models.DateTimeField(auto_now_add=True)
    user                    = models.ForeignKey(User, on_delete=models.CASCADE)
    isBestAnswer            = models.BooleanField(default=False)

    def __str__(self):
        return self.answer_description
        
