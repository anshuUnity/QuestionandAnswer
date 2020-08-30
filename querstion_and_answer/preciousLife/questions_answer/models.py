from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from taggit.managers import TaggableManager
from django.utils import timezone
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation


from django.contrib.auth import get_user_model
from accounts.models import UserProfileInfo
# QUESTION_ANSWER MODELS 
# Create your models here.

User = get_user_model()

class Question(models.Model, HitCountMixin):
    slug              =models.SlugField(max_length=264)
    title             =models.CharField(max_length=264, blank=False, null=False, unique=True)
    description       =models.TextField(max_length=None, blank=False, null=False)
    published_date    =models.DateTimeField()
    image_first       =models.ImageField(blank=True, null=True, upload_to = 'question_images')
    image_second      =models.ImageField(blank=True, null=True, upload_to ='question_images')
    image_third       =models.ImageField(blank=True, null=True, upload_to = 'question_images')
    user              =models.ForeignKey(User, on_delete=models.CASCADE, related_name='question')
    tags              =TaggableManager(blank=True, help_text='Give the tags to the question')
    likes             =models.ManyToManyField(User, related_name='likes', blank=True)
    hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation') 
 
    

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


class Answer(models.Model):
    questions               = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_description      = models.TextField(blank=False, null=False, verbose_name='answer_desc')
    published_at            = models.DateTimeField(auto_now_add=True)
    user                    = models.ForeignKey(User, on_delete=models.CASCADE)
    isBestAnswer            = models.BooleanField(default=False)

    def __str__(self):
        return self.answer_description
        
class ReportQuestion(models.Model):
    questions               = models.ForeignKey(Question, on_delete=models.CASCADE)
    report_description      = models.TextField(blank=True, null=True, max_length=264)
    user                    = models.ForeignKey(User, on_delete=models.CASCADE)
    question_url            = models.URLField(null=True, blank=True)

    def __str__(self):
        return "{} '@{}' ".format(self.questions.title, self.user.username)

class ReportAnswer(models.Model):
    questions               = models.ForeignKey(Question, on_delete=models.CASCADE)
    report_description      = models.TextField(blank=True, null=True, max_length=264)
    answers                 = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user                    = models.ForeignKey(User, on_delete=models.CASCADE)
    question_url            = models.URLField(null=True, blank=True)

    def __str__(self):
        return "{} '@{}' ".format(self.questions.title, self.user.username)