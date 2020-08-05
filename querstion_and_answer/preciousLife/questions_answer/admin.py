from django.contrib import admin
from questions_answer.models import Question, Images, Answer
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.

class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('description',)


class ImageAdmin(admin.ModelAdmin):
    list_display = ('question','image')
    

admin.site.register(Question, PostAdmin)
admin.site.register(Images, ImageAdmin)

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('answer_description','published_at','isBestAnswer','user','published_at')
    search_fields = ['answer_description']

admin.site.register(Answer, AnswerAdmin)