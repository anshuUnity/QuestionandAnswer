from django.db import models
from django.contrib import auth
from django.urls import reverse
from django.core.validators import RegexValidator

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
    user                = models.OneToOneField(to=auth.models.User, on_delete=models.CASCADE)
    website_instagram   = models.URLField(blank=True, null=True, default="",   validators=
                                    [RegexValidator(
                                        regex= '(?:https?:)?\/\/(?:www\.)?(?:instagram\.com|instagr\.am)\/(?P<username>[A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)',
                                        message='',
                                    )])
    website_twitter     = models.URLField(blank=True, null=True, default="", validators=                                    
                                    [RegexValidator(
                                        regex= '(?:https?:)?\/\/(?:[A-z]+\.)?twitter\.com\/@?(?P<username>\w+)\/?',
                                        message='',
                                    )])
    profile_pic         = models.ImageField(blank=True, upload_to = 'profile_pics')
    description         = models.TextField(blank=True, default='', null=True, max_length=250)
    full_name           = models.CharField(blank=True, max_length=230, null=True)
    gender              = models.CharField(max_length=100, blank=False, choices=COLOR_CHOICES, default='')


    def get_absolute_url(self):
        return reverse("home",kwargs={'pk':self.pk})

    def __str__(self):
        return self.user.username