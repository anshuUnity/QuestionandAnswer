from django.shortcuts import render
from django.views.generic import CreateView, ListView
from questions_answer.form import QuestionForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from hitcount.views import HitCountDetailView

from questions_answer.models import Question
from django.contrib.auth import get_user_model

User = get_user_model()

# QUESTION_ANSWER VIEWS.PY
# Create your views here.

@method_decorator(login_required, name='dispatch')
class CreateQuestion(CreateView):
    template_name = 'question_answer/create_question.html'
    message      = 'Thanks, You have successfully Posted The Question'
    form_class    = QuestionForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse('home')

class QuestionsList(ListView):
    model = Question
    template_name = 'index.html'
    

class QuestionDetail(HitCountDetailView):
    template_name = 'question_answer/question_detail.html'
    model = Question
    slug_field = 'slug'

    try:
        count_hit = True
    except:
        print('could not count the view')