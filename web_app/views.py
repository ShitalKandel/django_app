from django.shortcuts import render, redirect
# from django.contrib.auth import  login
from .models import UserProfile,Photo
from .forms import SignupForm,LoginForm,UserImage


def register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()   
            return redirect('web_app:login_success')  
    else:
        form = SignupForm()
    
    return render(request, 'register.html', {'form': form})




def login_success(request):
    return render(request, 'login_success.html')


def signIn(request):
    error_message = None

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # user = authenticate(request, username=username, password=password)
            user= UserProfile.objects.filter(email=email,password=password).first()
            if user:
                return redirect('web_app:login_success')
            else:
                error_message = "Invalid username or password."
    form = LoginForm()
    return render(request, 'login.html', {'form': form, 'error_message': error_message})


def profile(request):
    return redirect(request,'login_success')



def logout(request):
    
    return render(request,'logout.html')


def imagerequest(request):
    if request.method == 'POST':
        form = UserImage(request.POST,request.FILES)    
        
        if form.is_valid():
            form.save()

            img_obj = form.instance
            return render(request,'image.html',{'form':form,'img_obj':img_obj})
        
        else:
            form = UserImage()

    return render(request,'image.html',{'form':form})