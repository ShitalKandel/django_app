from django.urls import path
from web_app import views

app_name = "web_app"

urlpatterns=[
    path('register/',views.register,name="register"),
    path('login/', views.signIn, name='login'),
    path('success/',views.login_success,name="login_success"),
    path('logout/',views.logout,name="logout"),
    path('upload-image/',views.imagerequest,name="imagerequest"),
    # path('login/<int:id>',views.profile,name="profile"),
]