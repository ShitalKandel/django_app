from django import forms
from .models import UserProfile , Photo,Feeds

class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    # class Meta:
    #     model = UserProfile
    #     fields = ['first_name', 'last_name', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data

    def save(self):
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user = UserProfile.objects.create(first_name=first_name,last_name=last_name,email=email,password=password)
       
        return user 


class LoginForm(forms.Form):
    email = forms.EmailField(label="register-form",max_length=150)
    password = forms.CharField(label="register-form",widget=forms.PasswordInput)


class UserImage(forms.ModelForm):
    class Meta:#data of a parent data
        model = Photo
        fields = ('username','caption','imagefield',)


class New_post(forms.ModelForm):
    class Meta:
        model = Feeds
        fields = ['user_profile','name','user','comment']
    

