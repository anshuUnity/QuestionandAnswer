from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.views.generic import CreateView, ListView, DetailView
from questions_answer.form import QuestionForm, ImageForm, AnswerForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from hitcount.views import HitCountDetailView
from django.db.models import Q
from taggit.models import Tag
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Count
from notifications.signals import notify

from questions_answer.models import Question, Images, Answer
from django.contrib.auth import get_user_model
from accounts.models import UserProfileInfo
from django.forms import modelformset_factory

User = get_user_model()

# QUESTION_ANSWER VIEWS.PY
# Create your views here.

# @method_decorator(login_required, name='dispatch')
# class CreateQuestion(CreateView):
#     template_name = 'question_answer/create_question.html'
#     message      = 'Thanks, You have successfully Posted The Question'
#     form_class    = QuestionForm

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)

#     def get_success_url(self):
#         messages.success(self.request, self.message)
#         return reverse('home')

@login_required
def create_question_view(request):
    ImageFormSet = modelformset_factory(Images, fields=('image',), extra=3)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        formset = ImageFormSet(request.POST or None, request.FILES or None, queryset=Images.objects.none)
        if form.is_valid() and formset.is_valid():
            question_form = form.save(commit=False)
            question_form.user = request.user
            question_form.save()

            for f in formset:
                try:
                    photo = Images(question=question_form, image=f.cleaned_data['image'])
                    photo.save()
                except Exception as e:
                    break
            messages.success(request,'Question created successfully')
            return redirect('home')
    else:
        form = QuestionForm()
        formset = ImageFormSet(queryset=Images.objects.none())
    context = {
        'form':form,
        'formset':formset
    }

    return render(request, 'question_answer/create_question.html', context)

class QuestionsList(ListView):
    model = Question
    template_name = 'index.html' 
    context_object_name = 'questions'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trending_question = Question.objects.annotate(like_count=Count('likes')).order_by('-like_count')[:7]
        context['popular_tags'] = Question.tags.most_common()[:25]
        context['trending_question'] = trending_question
        return context


class QuestionDetail(HitCountDetailView):
    template_name = 'question_answer/question_detail.html'
    model = Question
    slug_field = 'slug'
    form_class = AnswerForm  

    try:
        count_hit = True
    except:
        print('could not count the view')

    def get_context_data(self, *args, **kwargs):
        question = get_object_or_404(Question, slug=self.kwargs['slug'])
        total_likes = question.total_likes()
        context = super().get_context_data(**kwargs)
        related_question = question.tags.similar_objects()
        context['total_likes'] = total_likes
        context['related_question'] = related_question
        return context


def LikeView(request, slug):
    question = get_object_or_404(Question, id=request.POST.get('question_id'))
    isliked = False
    if question.likes.filter(id=request.user.id).exists():
        question.likes.remove(request.user)
        isliked = False
    
    else:
        question.likes.add(request.user)
        isliked = True

    context = {
        'question':question,
        'total_likes': question.total_likes(),
        'isliked':isliked
    }

    if request.is_ajax():
        html = render_to_string('question_answer/_like_snippet.html', context, request=request)
        return JsonResponse({'form':html})

    # return HttpResponseRedirect(reverse('questions_answer:question_detail', args=[str(slug)]))

class AnswerFormClass(CreateView):
    model = Answer
    form_class = AnswerForm
    # success_url = ('question_answer:question_detail')
    template_name = 'question_answer/answer.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.questions_id = self.kwargs['pk']
        notify.send(form.instance.user, recipient=form.instance.questions.user, 
            verb='Answer Has Been posted To your Question')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('questions_answer:question_detail', kwargs={'slug': self.object.questions.slug})

class QuestionSearchView(QuestionsList):

    def get_queryset(self):
        result = super(QuestionSearchView, self).get_queryset()
        query = self.request.GET.get('q')

        if query:
            query_set = query.split(' ')

            for q in query_set:
                result = Question.objects.filter(
                    Q(description__icontains=q)|
                    Q(title__icontains=q)|
                    Q(tags__name__icontains=q)
                )
        if not result:
            messages.warning(self.request, 'No Records Found')
        return result

class SearchByTagView(ListView):
    model = Question
    template_name = 'question_answer/tag_list.html'
    context_object_name = 'questions'

    def get_queryset(self, **kwargs):

        return Question.objects.filter(tags__slug=self.kwargs['tag'])
 
     
