from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, Http404
from django.urls import reverse
from blog.forms import BlogForm
from blog.models import BlogPost
from django.views.generic import ListView, View, DetailView,UpdateView,DeleteView, CreateView
from hitcount.views import HitCountDetailView

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# Create your views here.

@method_decorator(login_required, name='dispatch')
class CreateBlog(CreateView):
    form_class = BlogForm
    template_name = 'blog/create_blog.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('home')

class BlogList(ListView):
    model = BlogPost
    template_name = 'blog/blog_list.html'
    context_object_name = 'blogs'

class BlogDetail(HitCountDetailView):
    template_name = 'blog/blog_detail.html'
    model = BlogPost
    slug_field = 'slug'

    try:
        count_hit = True
    except:
        print('could not count the view')