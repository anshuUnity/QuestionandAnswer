from django.views.generic import TemplateView
from django.shortcuts import render
from django.views.defaults import page_not_found

class HomePage(TemplateView):
    template_name = 'index.html'

class ThanksPage(TemplateView):
    template_name = 'thanks.html'

class TestPage(TemplateView):
    template_name = 'test.html'

def handler404(request, exception):
    return page_not_found(request, exception, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)