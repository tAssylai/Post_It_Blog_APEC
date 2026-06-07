from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('newpost/', views.newpost, name='newpost'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
]
