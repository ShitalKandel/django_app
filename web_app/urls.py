from django.urls import path,include
from web_app import views

app_name = "web_app"

urlpatterns=[
    path('register/',views.register,name="register"),
    path('login/', views.signIn, name='login'),
    path('success/',views.login_success,name="login_success"),
    path('logout/',views.logout,name="logout"),
    path('upload/',views.image_request,name="image_request"),
    path('uploaded/',views.upload_image,name="upload_image"),
    path('feed/',views.feed,name="feed"),
    # path('login/<int:id>',views.profile,name="profile"),
]