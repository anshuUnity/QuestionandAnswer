from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from accounts.models import UserProfileInfo
from django import forms

class SignUpForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = ""
        self.fields['email'].label = ""
        self.fields['password1'].label = ""
        self.fields['password2'].label = ""
        self.fields['username'].widget.attrs.update({'class' : 'myfieldclass'})
        self.fields['email'].widget.attrs.update({'class' : 'myfieldclass'})
        self.fields['password1'].widget.attrs.update({'class' : 'myfieldclass'})
        self.fields['password2'].widget.attrs.update({'class' : 'myfieldclass'})

        # giving place holders to fields
        self.fields['username'].widget.attrs.update({'placeholder':'Enter Your Username*'})
        self.fields['email'].widget.attrs.update({'placeholder':'Enter Your Email*'})
        self.fields['password1'].widget.attrs.update({'placeholder':'Password'})
        self.fields['password2'].widget.attrs.update({'placeholder':'Confirm Password'})


        for text in ['username', 'password1', 'password2']:
            self.fields[text].help_text = None


class UserProfileForm(forms.ModelForm):

    class Meta:
        model       = UserProfileInfo
        fields      = ('website', 'profile_pic', 'description', 'full_name')