from django.db import models
from django.contrib import auth
from django.urls import reverse

# Create your models here.
# ACCOUNTS MODELS

COLOR_CHOICES = (
    ('Male','Male'),
    ('Female', 'Female'),
    ('Others','others'),
)

class User(auth.models.User, auth.models.PermissionsMixin):

    def __str__(self):
        return "@{}".format(self.username)


class UserProfileInfo(models.Model):
    user        = models.OneToOneField(to=auth.models.User, on_delete=models.CASCADE)
    website_instagram   = models.URLField(blank=True, null=True, default="")
    website_twitter     = models.URLField(blank=True, null=True, default="")
    profile_pic = models.ImageField(blank=True, upload_to = 'profile_pics')
    description = models.TextField(blank=True, default='', null=True, max_length=250)
    full_name   = models.CharField(blank=True, max_length=230, null=True)
    gender      = models.CharField(max_length=100, blank=False, choices=COLOR_CHOICES, default='')


    def get_absolute_url(self):
        return reverse("home",kwargs={'pk':self.pk})

    def __str__(self):
        return self.user.username