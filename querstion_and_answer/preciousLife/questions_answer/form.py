from django import forms
from questions_answer.models import Question, Answer

class QuestionForm(forms.ModelForm):


    class Meta:
        model = Question
        fields = ('title', 'description', 'tags', 'image_first', 'image_second', 'image_third',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = ""
        self.fields['description'].label = ""
        self.fields['tags'].label = ""
        self.fields['image_first'].label = ""
        self.fields['image_second'].label = ""
        self.fields['image_third'].label = ""
        self.fields['title'].widget.attrs.update({'class' : 'question_title'})
        self.fields['description'].widget.attrs.update({'class' : 'question_description'})
        self.fields['tags'].widget.attrs.update({'class' : 'question_tags'})
        self.fields['image_first'].widget.attrs.update({'class' : 'question_image', 'id':'image_first'})
        self.fields['image_second'].widget.attrs.update({'class' : 'question_image', 'id':'image_second'})
        self.fields['image_third'].widget.attrs.update({'class' : 'question_image', 'id':'image_third'})


        # giving place holders to fields
        self.fields['title'].widget.attrs.update({'placeholder':'Title'})
        self.fields['description'].widget.attrs.update({'placeholder':'Description'})
        self.fields['tags'].widget.attrs.update({'placeholder':'Tags'})

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('answer_description',)
