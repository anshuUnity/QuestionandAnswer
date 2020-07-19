from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin

from django.contrib.auth.models import User

from accounts.forms import SignUpForm
from accounts.forms import UserProfileForm

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from accounts.models import UserProfileInfo

# Create your views here.
# ACCOUNTS VIEWS

class SignUp(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'
        

# def user_profile_edit(request):
#     user_profile = UserProfileForm
    
#     form = user_profile(request.POST or None, instance=request.user.userprofileinfo)
#     if request.method == 'POST':

        
#         # user_profile = UserProfileForm(data=request.POST, instance=request.user.userprofileinfo)

#         if form.is_valid():
            
#             if 'profile_pic' in request.FILES:
#                 form.profile_pic = request.FILES['profile_pic']
#             form.save()
#             form.user = request.user
#             return HttpResponseRedirect(reverse('home'))

#         else:
#             print(user_profile.errors)

#     else:
#         user_profile = UserProfileForm(instance=request.user.userprofileinfo)
#     return render(request, 'accounts/edit_profile.html', {'form':form})

@method_decorator(login_required, name='dispatch')
class EditProfile(UpdateView):
    model = UserProfileInfo
    fields = ['description', 'full_name', 'website', 'profile_pic']
    template_name = 'accounts/edit_profile.html'
    success_url = reverse_lazy('home')