from django import forms
from questions_answer.models import Question
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

class QuestionForm(forms.ModelForm):


    class Meta:
        model = Question
        fields = ('title', 'description', 'tags')
        widgets = {
            'description': SummernoteWidget
        }
        