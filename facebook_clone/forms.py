from django import forms
from facebook_clone.models import UserProfile, ImageUpload, Post, Comment, FriendRequest


class SignupForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    username = forms.CharField(max_length=150)  # Add username field

    class Meta:
        model = UserProfile
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


class UserImageForm(forms.ModelForm):
    class Meta:
        model = ImageUpload
        fields = ['caption', 'image']
        labels = {
            'image': 'Upload Image',
            'caption': 'Caption',
        }


class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['caption', 'image']
        labels = {
            'image': 'Upload Image',
            'caption': 'Caption',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {
            'text': 'Comment',
        }
        widgets = {
            'text': forms.TextInput(attrs={'placeholder': 'Add a comment...'}),
        }


class FriendRequestForm(forms.ModelForm):
    class Meta:
        model = FriendRequest
        fields = ['to_user','from_user']
