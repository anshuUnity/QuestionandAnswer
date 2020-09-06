from django.shortcuts import render, redirect
from django.views.generic import ListView, View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from questions_answer.models import Question
from blog.models import BlogPost

# Create your views here. NOTICE VIEWS

@method_decorator(login_required, name='dispatch')
class NotificationListView(ListView):
    "" "notification list" ""
    #Name of the context
    context_object_name = 'notices'
    template_name = 'notice/notice_list.html'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.request.user.notifications.unread()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        read = self.request.user.notifications.read()
        context['read'] = read

        return context

class UpdateNotificationView(View):
    
    def get(self, request):

        notice_id = request.GET.get('notice_id')
        post_id = request.GET.get('post_id')
        question_id = request.GET.get('question_id')
        #Update single notice
        if notice_id and question_id:
            question = Question.objects.get(id=question_id)
            request.user.notifications.get(id=notice_id).mark_as_read()
            return redirect(question)
        elif notice_id and post_id:
            blog =BlogPost.objects.get(id=post_id)
            request.user.notifications.get(id=notice_id).mark_as_read()
            return redirect(blog)
        else:
            request.user.notifications.mark_all_as_read()
            return redirect('notice:notice_list')
            