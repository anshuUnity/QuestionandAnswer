from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin

from django.contrib.auth.models import User

from accounts.forms import SignUpForm, ContactFormModel
from accounts.forms import UserProfileForm
from django.contrib.messages.views import SuccessMessageMixin

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from accounts.models import UserProfileInfo, ContactForm
from questions_answer.models import Question, Answer
from blog.models import BlogPost

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

    def get_object(self):
        return self.request.user.userprofileinfo

    def get_success_url(self):
        return reverse('accounts:profile_detail', kwargs={'pk': self.object.pk})

class ProfileDetail(DetailView):

    model = UserProfileInfo
    context_object_name = 'profile_detail'
    template_name = 'accounts/user_profile_page.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        user_question = Question.objects.filter(user = self.object.user).order_by('-published_date')
        user_answer = Answer.objects.filter(user = self.object.user).order_by('-published_at')
        user_blog = BlogPost.objects.filter(author = self.object.user).order_by('-published_date')

        if self.request.user.is_authenticated:
            save_blog = BlogPost.objects.filter(favorite=self.request.user)
            context['save_blog'] = save_blog

        context['user_question'] = user_question
        context['user_answer'] = user_answer
        context['user_blog'] = user_blog
        return context

@method_decorator(login_required, name='dispatch')
class ContactView(CreateView):
    model = ContactForm
    form_class = ContactFormModel
    template_name = 'accounts/contact.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('home')