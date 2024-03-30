from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('sign-up/', views.sign_up, name='sign-up'),
    path('create-post/', views.create_post, name='create-post'),
    path('delete-post/', views.delete_post, name='delete-post'),
    path('ban-user/', views.ban_user, name='ban-user'),
]