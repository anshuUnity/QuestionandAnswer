from django.urls import path
from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.CreateBlog.as_view(), name = 'create_blog'),
    path('blog-list/', views.BlogList.as_view(), name = 'blog_list'),
    path('blog-detail/<slug>/', views.BlogDetail.as_view(), name = 'blog_detail'),
]
