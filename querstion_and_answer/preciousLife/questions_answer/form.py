from django import forms
from questions_answer.models import Question, Images, Answer
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

class QuestionForm(forms.ModelForm):


    class Meta:
        model = Question
        fields = ('title', 'description', 'tags')
        widgets = {
            'description': SummernoteWidget(),
        }

class ImageForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ('image',)

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('answer_description','questions')
        widgets = {'questions': forms.HiddenInput()}
