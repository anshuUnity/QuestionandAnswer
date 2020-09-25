from django.urls import path
from questions_answer import views


app_name = 'questions_answer'

urlpatterns = [
    path('questions/', views.QuestionsList.as_view(), name = 'questions'),
    path('', views.CreateQuestion.as_view(), name='create'),
    path('question/description/<slug>/', views.QuestionDetail.as_view(), name='question_detail'),
    path('question/answer/create/<int:pk>', views.AnswerFormClass.as_view(), name='answer'),
    path('search/', views.QuestionSearchView.as_view(), name='qa_search'),
    path('tag/<tag>/', views.SearchByTagView.as_view(), name='qa_tag'),
    path('likes/<slug>/', views.LikeView, name='likes'),
    path('like/answer/', views.likeAnswer, name='answer_like'),
    path('update/<int:pk>/question/', views.QuestionUpdateView.as_view(), name='update_qa'),
    path('delete/question/<int:pk>', views.DeleteQuestion, name='qa_question_delete'),
    path('edit/<int:pk>/answer/', views.AnswerUpdateView.as_view(), name='qa_answer_update'),
    path('delete/<int:pk>/answer/', views.delete_answer, name='qa_answer_delete'),
    path('report/<int:pk>/question/', views.reportQuestion, name='qa_report_question'),
    path('report/<int:pk>/answer/', views.reportAnswer, name='qa_report_answer'),
    path('mark/<int:pk>/answer', views.mark_answer, name = 'mark_answer')
]
