from django.db.models.signals import post_save
from django.contrib.auth.models import User
#reciever
from django.dispatch import receiver
from accounts.models import UserProfileInfo

from guardian.shortcuts import assign_perm

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfileInfo.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.userprofileinfo.save()

