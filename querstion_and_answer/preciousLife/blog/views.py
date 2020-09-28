from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, Http404, redirect
from django.urls import reverse
from blog.forms import BlogForm, CommentBlogForm
from blog.models import BlogPost, CommentBlogPost
from django.views.generic import ListView, View, DetailView,UpdateView,DeleteView, CreateView
from hitcount.views import HitCountDetailView
from django.db.models import Q
from taggit.models import Tag
from django.contrib import messages

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic.edit import FormMixin
from notifications.signals import notify

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

from accounts.mixin import AjaxFormMixin

# Create your views here.

######################
# function based views
######################

@login_required
def like_blog(request, slug):
    blogpost = get_object_or_404(BlogPost, id=request.POST.get('blogpost_id'))

    if blogpost.likes.filter(id=request.user.id).exists():
        blogpost.likes.remove(request.user)
    
    else:
        blogpost.likes.add(request.user)

    context = {
        'blogpost':blogpost,
    }

    if request.is_ajax():
        html = render_to_string('blog/_like_snippet_blog_.html', context, request=request)
        return JsonResponse({'form':html})



@login_required
def save_blog(request, slug):
    blogpost = get_object_or_404(BlogPost, id = request.POST.get('blogpost_id'))

    if blogpost.favorite.filter(id=request.user.id).exists():
        blogpost.favorite.remove(request.user)
    
    else:
        blogpost.favorite.add(request.user)
    
    context = {
        'blogpost':blogpost
    }

    if request.is_ajax():
        html = render_to_string('blog/_save_blog_feed_.html', context, request=request)
        return JsonResponse({'form':html})

@login_required
def like_comment(request):
    comment = get_object_or_404(CommentBlogPost, id = request.POST.get('comment_id'))

    if comment.comment_like.filter(id=request.user.id).exists():
        comment.comment_like.remove(request.user)
        message = 'comment Disliked'

    else:
        comment.comment_like.add(request.user)
        message = 'comment Liked'

    response = {
        'comment':comment,
        'message': message,
    }

    # return redirect('blog:blog_detail', slug = comment.blogpost.slug)
    if request.is_ajax():
        htmly = render_to_string('blog/_like_comment_.html', response, request=request)
        return JsonResponse({'formly':htmly})

def delete_blog(request, pk):
    blog = get_object_or_404(BlogPost, pk=pk)



    if request.user != blog.author:
        return Http404()
    
    blog.delete()
    messages.success(request, "Blog Deleted Successfully", fail_silently=True)
    return redirect('home')

def delete_comment(request, pk):
    comment = get_object_or_404(CommentBlogPost, pk=pk)



    if request.user == comment.user or request.user == comment.blogpost.author:
        comment.delete()
        messages.success(request, "Comment Deleted", fail_silently=True)
    else:
        return Http404()
    
    return redirect('blog:blog_detail', slug = comment.blogpost.slug)

@method_decorator(login_required, name='dispatch')
class CreateBlog(CreateView):
    model = BlogPost
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
    paginate_by = 6

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        trending_blog = BlogPost.objects.order_by('-hit_count_generic__hits')[:7]
        context['popular_tags'] = BlogPost.blog_tags.most_common()[:25]
        context['trending_blog'] = trending_blog
        return context

@method_decorator(login_required, name='dispatch')
class BlogUpdateView(UpdateView):
    form_class = BlogForm
    model = BlogPost
    template_name = 'blog/update_blog.html'

    def get_queryset(self):
        query_set = super().get_queryset()
        queryset = query_set.filter(author = self.request.user)
        return queryset

    def get_success_url(self):
        return reverse('blog:blog_detail', kwargs={'slug':self.object.slug})

class BlogDetail(HitCountDetailView, FormMixin):
    template_name = 'blog/blog_detail.html'
    model = BlogPost
    slug_field = 'slug'
    form_class = CommentBlogForm

    try:
        count_hit = True
    except:
        print('could not count the view')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        blog = get_object_or_404(BlogPost, slug = self.kwargs['slug'])
        related_blog = blog.blog_tags.similar_objects()
        comments = CommentBlogPost.objects.filter(blogpost=self.object)
        context['comment_form'] = CommentBlogForm
        context['related_blog'] = related_blog
        context['comments'] = comments
        return context
    
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.blogpost = self.object

        if self.request.user != form.instance.blogpost.author:
            notify.send(form.instance.user,
                recipient=form.instance.blogpost.author,
                verb=u'Commented on your blog',
                description=form.instance.comment_content,
                target=form.instance.blogpost)


            plainText = get_template('blog/custom_email.txt')
            htmly = get_template('blog/custom_email.html')

            context = {
                'username':form.instance.user,
                'comment': form.instance.comment_content
            }
            subject, from_mail, to = 'Comment On a Blog', 'anshupal258@gmail.com', form.instance.blogpost.author.email
            text_content = plainText.render(context)
            html_content = htmly.render(context)
            msg = EmailMultiAlternatives(subject, text_content, from_mail, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send(fail_silently=False)


        form.save()
        response = {
            'message':'Form Submitted Successfully',
            'comments':CommentBlogPost.objects.filter(blogpost=self.object),
            'comment_form':form,
        }
        # messages.success(self.request, "Comment added successfully", fail_silently=True)
        if self.request.is_ajax():
            htmly = render_to_string('blog/_comment_feed_.html', context=response, request=self.request)
            return JsonResponse({'formly':htmly})

    def get_success_url(self):
        return reverse('blog:blog_detail', kwargs={'slug': self.object.slug})


class EditCommentBlog(UpdateView):
    model = CommentBlogPost
    form_class = CommentBlogForm
    template_name = 'blog/update_comment_blog.html'

    def get_queryset(self):
        query_set = super().get_queryset()
        queryset = query_set.filter(user = self.request.user)
        return queryset

    def get_success_url(self):
        return reverse('blog:blog_detail', kwargs={'slug':self.object.blogpost.slug})
    

class BlogSearchView(BlogList):

    def get_queryset(self):
        result = super(BlogSearchView, self).get_queryset()
        query = self.request.GET.get('q')

        if query:
            query_set = query.split(' ')

            for q in query_set:
                result = BlogPost.objects.filter(
                    Q(blog_description__icontains=q)|
                    Q(blog_title__icontains=q)|
                    Q(blog_tags__name__icontains=q)
                ).distinct()
        if not result:
            messages.warning(self.request, 'No Records Found')
        return result

class SearchByTagView(ListView):
    model = BlogPost
    template_name = 'blog/tag_list.html'
    context_object_name = 'blogpost'
    paginate_by = 6

    def get_queryset(self, **kwargs):
        return BlogPost.objects.filter(blog_tags__slug=self.kwargs['tag'])