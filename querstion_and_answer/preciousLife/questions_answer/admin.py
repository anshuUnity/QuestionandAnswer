from django.contrib import admin
from questions_answer.models import Question
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.

class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('description',)

admin.site.register(Question, PostAdmin)
