from django.urls import path
from apis import views

urlpatterns = [ 
    path('snippet/',views.snippet_list),
    path('snippets/<int:pk>',views.snippet_details),
    path('login-serializer/',views.UserLoginView.as_view()),
    path('register-serializer/',views.RegisterView.as_view()),
    path('reset-password/',views.ChangePasswordView.as_view()),
]