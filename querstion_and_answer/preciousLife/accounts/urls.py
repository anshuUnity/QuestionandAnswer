from django.urls import path
from django.contrib.auth import views as auth_views
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(),name='logout'),
    path('register/', views.SignUp.as_view(), name='register'),
    path('edit/profile/', views.EditProfile.as_view(), name = 'edit-profile'),
    path('profile/detail/<int:pk>', views.ProfileDetail.as_view(), name = 'profile_detail')
]