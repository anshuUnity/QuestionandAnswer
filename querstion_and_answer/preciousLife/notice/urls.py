from django.urls import path
from notice import views

app_name = 'notice'

urlpatterns = [
    path('notice-list/', views.NotificationListView.as_view(), name='notice_list'),
    path('notice_update/', views.UpdateNotificationView.as_view(), name='notice_update'),
]