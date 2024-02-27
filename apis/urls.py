from django.urls import path
from apis import views



urlpatterns = [ 
    path('snippet/',views.snippet_list),
    path('snippets/<int:pk>',views.snippet_detail),
    path('login/',views.UserLoginAPIView.as_view()),
    path('register/',views.RegisterAPIView.as_view()),
    path('reset-password/',views.ChangePasswordAPIView.as_view()),
    path("verify-otp/<str:phone>/", views.VerifyOTPAPIView.as_view()),
    path('items/',views.ItemListAPIView.as_view()),
    path('item/<int:pk>/',views.ItemDetailAPIView.as_view()),
    path('locations/',views.LocationListAPIView.as_view()),
    path('location/<int:pk>/',views.LocationDetailAPIView.as_view()),
]