from django.views.generic import TemplateView
from django.shortcuts import render
from django.views.defaults import page_not_found

class HomePage(TemplateView):
    template_name = 'index.html'

class ThanksPage(TemplateView):
    template_name = 'thanks.html'

class TestPage(TemplateView):
    template_name = 'test.html'

class PrivacyPolicy(TemplateView):
    template_name = 'policy_files/privacy_policy.html'

class CookiePolicy(TemplateView):
    template_name = 'policy_files/cookie_policy.html'

class TermsPolicy(TemplateView):
    template_name = 'policy_files/terms_condition.html'

class AboutView(TemplateView):
    template_name = 'policy_files/about.html'

def handler404(request, exception):
    return page_not_found(request, exception, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)