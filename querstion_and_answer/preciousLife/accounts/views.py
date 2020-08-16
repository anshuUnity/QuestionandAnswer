from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin

from django.contrib.auth.models import User

from accounts.forms import SignUpForm
from accounts.forms import UserProfileForm
from django.contrib.messages.views import SuccessMessageMixin

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from accounts.models import UserProfileInfo
from questions_answer.models import Question, Answer


# Create your views here.
# ACCOUNTS VIEWS

class SignUp(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'

        

@method_decorator(login_required, name='dispatch')
class EditProfile(SuccessMessageMixin ,UpdateView):
    model = UserProfileInfo
    # fields = ['description', 'full_name', 'website', 'profile_pic', 'gender',]
    template_name = 'accounts/edit_profile.html'
    form_class = UserProfileForm
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user.userprofileinfo

class ProfileDetail(DetailView):

    model = UserProfileInfo
    context_object_name = 'profile_detail'
    template_name = 'accounts/user_profile_page.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        user_question = Question.objects.filter(user = self.object.user).order_by('-published_date')[:3]
        user_answer = Answer.objects.filter(user = self.object.user).order_by('-published_at')[:3]
        context['user_question'] = user_question
        context['user_answer'] = user_answer
        return context

