from django.urls import path
from . import views

urlpatterns = [
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/<int:notif_id>/read/', views.mark_read, name='mark_read'),
]
