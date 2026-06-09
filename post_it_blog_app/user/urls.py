from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginsign, name='loginsign'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('<str:username>/', views.user_profile, name='user_profile'),
    path('<str:username>/follow/', views.follow_toggle, name='follow_toggle'),
    path('settings/', views.settings_view, name='settings'),
]