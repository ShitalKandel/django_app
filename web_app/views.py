from django.shortcuts import render, redirect
# from django.contrib.auth import  login
from .models import UserProfile,Photo, Feeds
from .forms import SignupForm,LoginForm,UserImage,New_post


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
    form = UserImage(request.POST, request.FILES)
    if form.is_valid():
        form = form.save
    return render(request, 'login_success.html',{'form':form})


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


def image_request(request):
    image = UserImage.objects.__dict__.get.__all__

    form = UserImage()
    if request.method == 'POST':
        form = UserImage(request.POST, request.FILES)    
        
        if form.is_valid():
            image = form.save()

            return render(request,'image.html',{'image':image})
        
    else:
        form = UserImage()

    return render(request,'image.html',{'form':form})


def upload_image(request,image_id):
    try:
        image = Photo.objects.get(pk=image_id)
    
    except Photo.DoesNotExist:
        return redirect('image not found')
    
    if request.method == 'POST':
        form = UserImage(request.POST,request.FILES,instance=image)
        if form.is_valid():
            form.save()
            return redirect('image_request')
    else:
        form = UserImage(instance=image)
        return render(request,'image.html',{'form':form,'image':image})
    

def create_post(request):
    return render(request,'home_page.html')

def post(request, first_name, last_name):
    user_profile = UserProfile.objects.get(first_name=first_name, last_name=last_name)
    if request.method == 'POST':
        form = New_post(request.POST)
        if form.is_valid():
            feed = form.save(commit=False)
            feed.user_profile = user_profile
            feed.save()
            return redirect(f'/{user_profile.first_name}_{user_profile.last_name}/')
    else:
        form = New_post()

    feeds = Feeds.objects.filter(user_profile=user_profile)
    return render(request, 'post.html', {'user_profile': user_profile, 'feeds': feeds, 'form': form})



def left_Profile_Bar(request):
    return render(request,'left_side_profilebar.html' )


def right_Profile_Bar(request):
    return render(request,'right_side_profilebar.html' )