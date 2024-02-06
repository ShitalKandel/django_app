from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



# Create your models here.
class signupform(UserCreationForm):
    firstname = forms.CharField(max_length=100)
    lastname = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)

    class meta:
        meta = User
        fields = ('Username','email','password','reset-password','firstname','lastname')


    def save(self,commit=True):
        # user = (signupform,self).save(commit=Flase)
        pass


# class loginform(User):
#     username = forms.request['username']
#     password = forms.request['password']
#     if username and password in UserCreationForm:
#         # return render()
#         pass
    
    

        