
from django.urls import path
from .views import (
    home_view,
    post_view,
    create_view,
    author_view,
    about_view,
    login_view,
    logout_view,
    register_view,
    edit_view,
    delete_view
)

# app_name = 'blog'

urlpatterns = [
    path('', home_view, name='home'),
    path('post/<str:pk>', post_view, name='post'),
    path('create/', create_view, name='create'),
    path('delete/<int:pk>', delete_view, name='delete'),
    path('author/<int:pk>', author_view, name='author'),
    path('edit/<str:pk>', edit_view, name='edit'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),

    
] 