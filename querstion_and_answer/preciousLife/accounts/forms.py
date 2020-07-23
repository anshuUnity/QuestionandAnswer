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
        fields      = ('full_name', 'gender', 'description', 'website_instagram', 'website_twitter', 'profile_pic')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


              # giving place holders to fields
        self.fields['website_instagram'].widget.attrs.update({'placeholder':'Instagram Link'})
        self.fields['website_twitter'].widget.attrs.update({'placeholder':'Twitter Link'})
        self.fields['profile_pic'].widget.attrs.update({'placeholder':''})
        self.fields['description'].widget.attrs.update({'placeholder':'Description'})
        self.fields['full_name'].widget.attrs.update({'placeholder':'Full Name'})

        self.fields['profile_pic'].widget.attrs.update({'class' : 'profile_preview_edit_profile', 'id':'profile_preview_edit_profile_id'})
        self.fields['website_instagram'].widget.attrs.update({'class' : 'edit_profile_website_instagram'})
        self.fields['website_twitter'].widget.attrs.update({'class' : 'edit_profile_website_instagram'})
        self.fields['description'].widget.attrs.update({'class' : 'edit_profile_description'})
        self.fields['full_name'].widget.attrs.update({'class' : 'edit_profile_website_instagram'})
        self.fields['gender'].widget.attrs.update({'class' : 'edit_profile_gender'})


        self.fields['website_twitter'].label = ""
        self.fields['website_instagram'].label = ""
        self.fields['description'].label = ""
        self.fields['full_name'].label = ""
