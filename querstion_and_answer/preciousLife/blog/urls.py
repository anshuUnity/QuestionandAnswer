from django.urls import path
from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.CreateBlog.as_view(), name = 'create_blog'),
    path('blog-list/', views.BlogList.as_view(), name = 'blog_list'),
    path('blog-detail/<slug>/', views.BlogDetail.as_view(), name = 'blog_detail'),
    path('search/blog/', views.BlogSearchView.as_view(), name='blog_search'),
    path('tags/blog/<tag>/', views.SearchByTagView.as_view(), name = 'blog_tag'),
    path('update/<int:pk>/blog/', views.BlogUpdateView.as_view(), name = 'blog_update'),
    path('delete/<int:pk>/blog/', views.delete_blog, name = 'blog_delete'),
    path('likes/<slug>/', views.like_blog, name = 'likes'),
    path('favorite/<slug>/', views.save_blog, name= 'save_blog'),
    path('edit/<int:pk>/comment/', views.EditCommentBlog.as_view(), name='edit_blog_comment'),
    path('delete/<int:pk>/comment', views.delete_comment, name = 'delete_blog_comment')
]
