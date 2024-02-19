from django.urls import path
from . import views

app_name = 'web_app'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout, name='logout'),
    path('login_success/', views.login_success, name='login_success'),
    path('upload_image/', views.upload_image, name='upload_image'),
    path('create_post/', views.create_post, name='create_post'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('add_friend/', views.add_friend, name='add_friend'),
    path('accept_friend_request/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('reject_friend_request/<int:request_id>/', views.reject_friend_request, name='reject_friend_request'),
]
