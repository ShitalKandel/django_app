from django.urls import path
from apis import views

urlpatterns = [ 
    path('snippet/',views.snippet_list),
    path('snippets/<int:pk>',views.snippet_detail),
    path('login-serializer/',views.UserLoginView.as_view()),
    path('register-serializer/',views.RegisterView.as_view()),
    path('reset-password/',views.ChangePasswordView.as_view()),
    path("<phone>/", views.VerifyOTPView.as_view()),
    # path("your-otp/", views.Generate_OTP.as_view()),
]