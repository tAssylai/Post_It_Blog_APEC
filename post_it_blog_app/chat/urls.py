from django.urls import path
from . import views

urlpatterns = [
    path('messages/', views.inbox, name='inbox'),
    path('messages/<int:conversation_id>/', views.conversation, name='conversation'),
    path('messages/start/<str:username>/', views.start_conversation, name='start_conversation'),
]
