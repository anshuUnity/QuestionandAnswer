from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from questions_answer.models import Question, Answer, ReportQuestion, ReportAnswer
# Register your models here.


class ImageAdmin(admin.ModelAdmin):
    list_display = ('question','image')
    

admin.site.register(Question)

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('answer_description','published_at','isBestAnswer','user','published_at')
    search_fields = ['answer_description', 'user__username']

admin.site.register(Answer, AnswerAdmin)

class ReportQuestionAdmin(admin.ModelAdmin):
    list_display = ('questions', 'user', 'question_url')
    search_fields = ['user__username', 'questions__title']
    list_filter = (
        ('questions', DateFieldListFilter),
    )

admin.site.register(ReportQuestion, ReportQuestionAdmin)

class ReportAnswerAdmin(admin.ModelAdmin):
    list_display = ('questions', 'user', 'question_url', 'answers',)
    search_fields = ['user__username', 'questions__title']
    list_filter = (
        ('questions', DateFieldListFilter),
    )

admin.site.register(ReportAnswer, ReportAnswerAdmin)