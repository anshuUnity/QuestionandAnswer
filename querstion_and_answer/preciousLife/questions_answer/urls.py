from django.urls import path
from questions_answer import views


app_name = 'questions_answer'

urlpatterns = [
    path('', views.create_question_view, name='create'),
    # path('list/', views.QuestionsList.as_view(), name='list'),
    path('question/description/<slug>/', views.QuestionDetail.as_view(), name='question_detail'),
    path('question/answer/create/<int:pk>', views.AnswerFormClass.as_view(), name='answer'),
    path('search/', views.QuestionSearchView.as_view(), name='qa_search'),
    path('tag/<tag>/', views.SearchByTagView.as_view(), name='qa_tag'),
    path('likes/<slug>/', views.LikeView, name='likes'),
]
