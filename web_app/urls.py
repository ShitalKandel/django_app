from django.urls import path
from web_app import views

app_name = "web_app"

urlpatterns=[
    path('register/',views.register,name="register"),
    path('login/', views.signIn, name='login'),
    path('success/',views.login_success,name="login_success"),
    path('register/',views.new_account,name="new_account"),
]