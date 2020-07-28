from django.urls import path
from questions_answer import views


app_name = 'questions_answer'

urlpatterns = [
    path('', views.CreateQuestion.as_view(), name='create'),
    # path('list/', views.QuestionsList.as_view(), name='list'),
    path('question/description/<slug>/', views.QuestionDetail.as_view(), name='question_detail')
]
