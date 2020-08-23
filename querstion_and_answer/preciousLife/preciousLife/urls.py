"""preciousLife URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from preciousLife import main_views
from questions_answer import views
from django.contrib.auth import views as auth_views

from preciousLife import settings
from django.conf.urls.static import static
import notifications.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.QuestionsList.as_view(), name='home'),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('test/', main_views.TestPage.as_view(), name='test'),
    path('thanks/', main_views.ThanksPage.as_view(), name='thanks'),
    path('questions_answer/', include('questions_answer.urls')),
    path('blog/', include('blog.urls')),
    path('notice/', include('notice.urls', namespace='notice')),

    path('hitcount/', include('hitcount.urls', namespace='hitcount')),

    path('summernote/', include('django_summernote.urls')),

    path('inbox/notifications/', include(notifications.urls, namespace='notifications')),
    # password reset views
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), 
        name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html'), 
        name='password_change'),

    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_done.html'),
     name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), 
        name='password_reset_confirm'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset_form.html'), name='password_reset'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
     name='password_reset_complete'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
# handler404 = main_views.handler404
# handler500 = main_views.handler500