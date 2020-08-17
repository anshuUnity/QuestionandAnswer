from django.contrib import admin
from questions_answer.models import Question, Images, Answer
# Register your models here.


class ImageAdmin(admin.ModelAdmin):
    list_display = ('question','image')
    

admin.site.register(Question)
admin.site.register(Images, ImageAdmin)

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('answer_description','published_at','isBestAnswer','user','published_at')
    search_fields = ['answer_description']

admin.site.register(Answer, AnswerAdmin)