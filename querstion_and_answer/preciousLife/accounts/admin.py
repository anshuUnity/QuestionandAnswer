from django.contrib import admin
from accounts.models import UserProfileInfo, ContactForm

# Register your models here.

class MyModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'pk')
    search_fields = ('user__username',)

admin.site.register(UserProfileInfo, MyModelAdmin)

class ContactModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'msg_subject', 'pk')
    search_fields = ('user__username', 'email')

admin.site.register(ContactForm, ContactModelAdmin)