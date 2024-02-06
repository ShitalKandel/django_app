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
        user = super(signupform,self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.firstname = self.cleaned_data['firstname']
        user.lastname = self.cleaned_data['lastname']

        if commit:
            user.save()

        return user

        


class loginform(User):

        pass
    
    

        