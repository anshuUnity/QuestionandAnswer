from django.contrib import admin
from accounts.models import UserProfileInfo


# Register your models here.

class MyModelAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserProfileInfo, MyModelAdmin)
