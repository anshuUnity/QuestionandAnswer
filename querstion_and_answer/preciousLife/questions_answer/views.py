from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect, Http404
from django.core.exceptions import ValidationError
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, View
from django.views.generic.list import MultipleObjectMixin
from questions_answer.form import QuestionForm, AnswerForm, ReportQuestionForm, ReportAnswerForm
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
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template


from questions_answer.models import Question, Answer, ReportQuestion
from django.contrib.auth import get_user_model
from accounts.models import UserProfileInfo

User = get_user_model()

# QUESTION_ANSWER VIEWS.PY
# Create your views here.

@method_decorator(login_required, name='dispatch')
class CreateQuestion(CreateView):
    template_name = 'question_answer/create_question.html'
    message      = 'Thanks, You have successfully Posted The Question'
    form_class    = QuestionForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse('questions_answer:questions')

@login_required
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

def likeAnswer(request):
    answer = get_object_or_404(Answer, id = request.POST.get('answer_id'))
    isLiked = False

    if answer.answer_likes.filter(id = request.user.id).exists():
        answer.answer_likes.remove(request.user)
        isLiked = False
        message = 'Answer disliked'

    else:
        answer.answer_likes.add(request.user)
        isLiked = True
        message = 'Answer liked'

    response = {
        'message':message,
        'total_likes':answer.answer_likes.count(),
        'isLiked':isLiked
    }

    # return redirect('questions_answer:question_detail', answer.questions.slug)
    return JsonResponse(response)

def mark_answer(request, pk):
    answer = get_object_or_404(Answer, pk=pk)

    if request.user != answer.questions.user:
        raise ValidationError("Only Author of the question is allowed to mark the answer")
    else:
        answer.questions.answer_set.update(isBestAnswer=False)
        answer.isBestAnswer = True
        answer.save()
        messages.success(request, "Answer Marked as best answer", fail_silently=True)
    return redirect('questions_answer:question_detail', answer.questions.slug)

def DeleteQuestion(request, pk):
    question = get_object_or_404(Question, pk=pk)

    if request.user != question.user:
        return Http404()
    
    question.delete()

    messages.success(request, 'Question Deleted Successfully', fail_silently=True)
    return redirect('questions_answer:questions')

def delete_answer(request, pk):
    answer = get_object_or_404(Answer, pk=pk)
    
    if request.user == answer.user or request.user == answer.questions.user:
        answer.delete()

    else:
        return Http404()
    
    messages.success(request, "Answer Deleted Successfully", fail_silently=True)
    return redirect('questions_answer:question_detail', slug=answer.questions.slug)

def reportQuestion(request, pk):
    question = get_object_or_404(Question, pk=pk)

    # correct way to get url of a previous page
    if request.method == 'GET':
        request.session['report_url'] = request.META.get('HTTP_REFERER')
    
    if request.method == 'POST':
        
        report_form = ReportQuestionForm(request.POST or None)
        if report_form.is_valid():
            
            new_form = report_form.save(commit=False)
            new_form.questions = question
            new_form.user = request.user
            new_form.question_url = request.session.get('report_url')
            new_form.save()
            messages.success(request, "Question Reported Successfully", fail_silently=True)
            return redirect('questions_answer:question_detail', slug=question.slug)

    else:
        report_form = ReportQuestionForm()

    context = {
        'form':report_form
    }
    return render(request, 'question_answer/report_question.html', context)    
    
def reportAnswer(request, pk):
    answer = get_object_or_404(Answer, pk=pk)

    # correct way to get url of a previous page
    if request.method == 'GET':
        request.session['report_url'] = request.META.get('HTTP_REFERER')
    
    if request.method == 'POST':
        
        report_form = ReportAnswerForm(request.POST or None)
        if report_form.is_valid():
            
            new_form = report_form.save(commit=False)
            new_form.questions = answer.questions
            new_form.user = request.user
            new_form.answers = answer
            new_form.question_url = request.session.get('report_url')
            new_form.save()
            messages.success(request, "Answer Reported Successfully", fail_silently=True)
            return redirect('questions_answer:question_detail', slug=answer.questions.slug)

    else:
        report_form = ReportQuestionForm()

    context = {
        'form':report_form
    }
    return render(request, 'question_answer/report_answer.html', context)    

#################
##CLASS BASED VIEWS##
##################
class QuestionsList(ListView):
    model = Question
    template_name = 'index.html' 
    context_object_name = 'questions'
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trending_question = Question.objects.order_by('-hit_count_generic__hits')[:10]
        context['popular_tags'] = Question.tags.most_common()[:25]
        context['trending_question'] = trending_question
        return context


class QuestionDetail(HitCountDetailView, MultipleObjectMixin):
    template_name = 'question_answer/question_detail.html'
    model = Question
    slug_field = 'slug'
    form_class = AnswerForm
    paginate_by = 6  

    try:
        count_hit = True
    except:
        print('could not count the view')

    def get_context_data(self, *args, **kwargs):
        question = get_object_or_404(Question, slug=self.kwargs['slug'])
        total_likes = question.total_likes()
        object_list = Answer.objects.filter(questions=self.get_object()).order_by('-published_at')
        context = super().get_context_data(object_list=object_list, **kwargs) #created object_list specially for pagination of answers
        related_question = question.tags.similar_objects()
        context['total_likes'] = total_likes
        context['related_question'] = related_question
        return context

class AnswerFormClass(CreateView):
    model = Answer
    form_class = AnswerForm
    # success_url = ('question_answer:question_detail')
    template_name = 'question_answer/answer.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.questions_id = self.kwargs['pk']

        if self.request.user != form.instance.questions.user:
            notify.send(form.instance.user, recipient=form.instance.questions.user, 
                verb=u'has answered your question', 
                description=form.instance.answer_description, 
                target=form.instance.questions)

            plainText = get_template('question_answer/custom_email.txt')
            htmly = get_template('question_answer/custom_email.html')

            context = {
                'username':form.instance.user,
                'answer': form.instance.answer_description
            }
            subject, from_mail, to = 'Answered your Question', 'anshupal258@gmail.com', form.instance.questions.user.email
            text_content = plainText.render(context)
            html_content = htmly.render(context)
            msg = EmailMultiAlternatives(subject, text_content, from_mail, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send(fail_silently=False)

            # send_mail(
            #     'Answered your Question',
            #     message,
            #     'anshupal258@gmail.com',
            #     [form.instance.questions.user.email],
            #     fail_silently=False,
            # )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('questions_answer:question_detail', kwargs={'slug': self.object.questions.slug})

@method_decorator(login_required, name='dispatch')
class AnswerUpdateView(UpdateView):
    form_class = AnswerForm
    model = Answer
    template_name = 'question_answer/answer_update.html'

    def get_queryset(self): 
        query_set = super().get_queryset()
        queryset = query_set.filter(user = self.request.user)
        return queryset

    def get_success_url(self):
        return reverse('accounts:profile_detail', kwargs={'pk':self.object.user.userprofileinfo.pk})

@method_decorator(login_required, name='dispatch')
class QuestionUpdateView(UpdateView):
    form_class = QuestionForm
    model = Question
    template_name = 'question_answer/update_question.html'

    def get_queryset(self): 
        query_set = super().get_queryset()
        queryset = query_set.filter(user = self.request.user)
        return queryset


    def get_success_url(self):
        return reverse('questions_answer:question_detail', kwargs={'slug':self.object.slug})


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
                ).distinct()
        if not result:
            messages.warning(self.request, 'No Records Found')
        return result
        

class SearchByTagView(ListView):
    model = Question
    template_name = 'question_answer/tag_list.html'
    context_object_name = 'questions'
    paginate_by = 2

    def get_queryset(self, **kwargs):

        return Question.objects.filter(tags__slug=self.kwargs['tag'])


